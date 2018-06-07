from django.conf import settings
from django.http import JsonResponse
from django.views import View

from temba_client.v2 import TembaClient

from lebombo.randomize_survey_utils import (
    assign_survey,
    get_first_question_id_and_text,
    get_next_question,
    check_answer,
)


DELIMITER = ";"


class InvestigationView(View):
    def get(self, request, investigation_slug, *args, **kwargs):
        # TODO: get this from cache, rather than constant
        import json
        import copy

        investigation_data = {}

        with open("lebombo/tests/test_investigation.json") as json_data:
            d = json.load(json_data)
            investigation_data = copy.deepcopy(d)
        # end

        update_rapidpro = True

        data = request.GET.dict()

        user_uuid = data["uuid"]

        investigation_field_key = investigation_data["investigation_key"]
        question_order_key = investigation_data["question_order_key"]

        client = TembaClient(investigation_data["url"], settings.RAPIDPRO_API_KEY)

        if ("start" in data) and (data["start"].lower() == "true"):
            language = data["language"] if data["language"] else None

            survey_id = assign_survey(investigation_data, language)

            if update_rapidpro:
                response = client.update_contact(
                    user_uuid, fields={investigation_field_key: survey_id}
                )
            # select a question from pool
            question_id, question_text = get_first_question_id_and_text(
                investigation_data, survey_id
            )

            # send the question id asked, in question order
            if update_rapidpro:
                response = client.update_contact(
                    user_uuid, fields={question_order_key: question_id}
                )

            resp = {
                "survey_id": survey_id,
                "question_id": question_id,
                "question_text": question_text,
                "question_order": question_id,
            }

            return JsonResponse(resp)

        else:
            # process their answer
            survey_id = data["survey_id"]
            current_question_text = data["question_text"]
            current_question_id = data["question_id"]
            response = data["response"]
            question_order = data["question_order"].split(DELIMITER)

            is_valid_answer, clean_answer, validation_error = check_answer(
                investigation_data, survey_id, current_question_id, response
            )

            if not is_valid_answer:
                return JsonResponse(
                    {
                        "valid": "answer_invalid",
                        "message": current_question_text,
                        "invalid_message": validation_error,
                        "question_order": question_order,
                        "is_finished": "not_finished",
                        "question_id": question_id,
                    }
                )

            # send answer to the label
            if update_rapidpro:
                client.update_contact(
                    user_uuid,
                    fields={current_question_id.replace("__", "_"): clean_answer},
                )

            question_id, question_text = get_next_question(
                investigation_data, survey_id, question_order
            )

            finished = not (bool(question_id) and bool(question_text))

            if finished:
                return JsonResponse(
                    {"valid": "answer_valid", "is_finished": "finished"}
                )

            question_order.append(question_id)
            question_order_representation = question_order[0]

            for question_id in question_order[1:]:
                question_order_representation = "{}{}{}".format(
                    question_order_representation, DELIMITER, question_id
                )

            if update_rapidpro:
                client.update_contact(
                    user_uuid,
                    fields={question_order_key: question_order_representation},
                )

            resp = {
                "valid": "answer_valid",
                "status": "not_finished",
                "question_text": question_text,
                "question_order": question_order_representation,
                "is_finished": "not_finished",
                "question_id": question_id,
            }

            return JsonResponse(resp)
