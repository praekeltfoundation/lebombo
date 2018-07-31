import random
import json


def get_survey_ids(investigation_data):
    return list(investigation_data["surveys"].keys())


def assign_survey(investigation_data, language):
    """
    return id based on language or randomly.
    """
    survey_ids = get_survey_ids(investigation_data)

    if language:
        # TODO: implement survey selection based on language
        pass

    return random.choice(survey_ids)


def get_question_ids_and_texts(investigation_data, survey_id):
    survey_data = investigation_data["surveys"][survey_id]
    result = {}
    for question_id, question_data in survey_data.items():
        result[question_id] = question_data["text"]
    return result


def get_first_question_id_and_text(investigation_data, survey_id):
    """
    gets any question from the survey and returns id and text
    """
    questions = get_question_ids_and_texts(investigation_data, survey_id)
    question_id = random.choice(list(questions.keys()))
    return (question_id, questions[question_id])


def get_next_question(investigation_data, survey_id, question_order):
    survey_questions = investigation_data["surveys"][survey_id]
    question_ids = list(survey_questions.keys())

    for question_id in question_order:
        question_ids.remove(question_id)

    if question_ids == []:
        return (None, None)

    new_question_id = random.choice(question_ids)
    return (new_question_id, survey_questions[new_question_id]["text"])


def get_current_question_id(investigation_data, survey_id, current_question_text):
    questions = investigation_data[survey_id]
    for key, question_data in questions.items():
        if question_data["text"] == current_question_text:
            return key


def get_validator_ids_from_ref(validator_refs):
    result = []
    for validator in validator_refs:
        result.append(validator["validator_id"])
    return result


def get_numeric_response(value):
    try:
        value = int(value)
        return value

    except ValueError:
        return None


def check_answer(investigation_data, survey_id, question_id, response):
    """
    is_valid_answer, clean_answer, validation_error
    """

    validator_refs = investigation_data["surveys"][survey_id][question_id]["validators"]
    validator_ids = get_validator_ids_from_ref(validator_refs)

    # check the order values
    # WARNING: assumption that we use numbers

    numeric_result = get_numeric_response(response)

    if numeric_result:
        if (0 < numeric_result) and (numeric_result <= len(validator_ids)):
            # return (is_valid_answer, clean_answer, validation_error)
            return (True, validator_ids[numeric_result - 1], False)

        else:
            # TODO: update this to handle more than one language
            return (False, None, "Number given is not valid")

    response = response.lower()
    validators = [
        investigation_data["validators"][validator_id] for validator_id in validator_ids
    ]
    for validator_id, validator in zip(validator_ids, validators):
        if "is_numeric" in validator:
            break

        if response in validator["options"]:
            return (True, validator_id, None)

    # TODO: update this to handle more than one language
    return (False, None, "Invalid answer, please try again")


def get_validator_ids(investigation_data):
    result = set()
    for survey, questions in investigation_data["surveys"].items():
        for question_id, question_data in questions.items():
            for validator_data in question_data["validators"]:
                set.add(validator_data["validator_id"])
    return result


def get_current_question(rapidpro_data):
    """
    Returns the current question text
    """
    steps = rapidpro_data["steps"]
    step = json.loads(steps)[1]
    return step["text"]
