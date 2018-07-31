import copy
import json

from django.test import TestCase
from lebombo.randomize_survey_utils import (
    get_survey_ids,
    assign_survey,
    get_question_ids_and_texts,
    get_first_question_id_and_text,
    get_next_question,
    get_validator_ids_from_ref,
    check_answer,
)


class TestSurveyUtils(TestCase):
    def setUp(self):
        with open("lebombo/tests/test_investigation.json") as json_data:
            self.inv_data = copy.deepcopy(json.load(json_data))

    def test_get_survey_ids(self):
        result = get_survey_ids(self.inv_data)
        self.assertEqual(type(result), list)
        self.assertEqual(
            result,
            [
                "inv_1__survey_1",
                "inv_1__survey_2",
                "inv_1__survey_3",
                "inv_1__survey_4",
                "inv_1__survey_5",
                "inv_1__survey_6",
            ],
        )

    def test_assign_survey(self):
        language = None
        survey_id = assign_survey(self.inv_data, language)
        self.assertTrue(
            survey_id
            in [
                "inv_1__survey_1",
                "inv_1__survey_2",
                "inv_1__survey_3",
                "inv_1__survey_4",
                "inv_1__survey_5",
                "inv_1__survey_6",
            ]
        )

    def test_get_question_ids_and_texts_1(self):
        expected_output = {
            "inv_1__survey_1__question_1": "Circumcision is good?\n1)Agree\n2)Disagree",
            "inv_1__survey_1__question_2": "Breastfeeding is good\n1)Agree\n2)Disagree",
            "inv_1__survey_1__question_3": "What is your favourite color?\n1)Blue\n2)Yellow\n3)Red",
            "inv_1__survey_1__question_4": "What is your favourite fruit?\n1)Apple\n2)Pear\n3)Banana",
            "inv_1__survey_1__question_5": "What is your age?\n1)0-12\n2)13-30\n3)31+",
        }
        self.assertEqual(
            get_question_ids_and_texts(self.inv_data, "inv_1__survey_1"),
            expected_output,
        )

    def test_get_question_ids_and_texts_2(self):
        expected_output = {
            "inv_1__survey_2__question_1": "Circumcision is good?\n1)Disagree\n2)Agree",
            "inv_1__survey_2__question_2": "Breastfeeding is good\n1)Disagree\n2)Agree",
            "inv_1__survey_2__question_3": "What is your favourite color?\n1)Red\n2)Blue\n3)Yellow",
            "inv_1__survey_2__question_4": "What is your favourite fruit?\n1)Banana\n2)Apple\n3)Pear",
            "inv_1__survey_2__question_5": "What is your age?\n1)0-12\n2)13-30\n3)31+",
        }
        self.assertEqual(
            get_question_ids_and_texts(self.inv_data, "inv_1__survey_2"),
            expected_output,
        )

    def test_get_first_question_id_and_text_1(self):
        result = get_first_question_id_and_text(self.inv_data, "inv_1__survey_1")
        self.assertTrue(
            result
            in [
                (
                    "inv_1__survey_1__question_1",
                    "Circumcision is good?\n1)Agree\n2)Disagree",
                ),
                (
                    "inv_1__survey_1__question_2",
                    "Breastfeeding is good\n1)Agree\n2)Disagree",
                ),
                (
                    "inv_1__survey_1__question_3",
                    "What is your favourite color?\n1)Blue\n2)Yellow\n3)Red",
                ),
                (
                    "inv_1__survey_1__question_4",
                    "What is your favourite fruit?\n1)Apple\n2)Pear\n3)Banana",
                ),
                (
                    "inv_1__survey_1__question_5",
                    "What is your age?\n1)0-12\n2)13-30\n3)31+",
                ),
            ]
        )

    def test_get_first_question_id_and_text_2(self):
        result = get_first_question_id_and_text(self.inv_data, "inv_1__survey_2")
        self.assertTrue(
            result
            in [
                (
                    "inv_1__survey_2__question_1",
                    "Circumcision is good?\n1)Disagree\n2)Agree",
                ),
                (
                    "inv_1__survey_2__question_2",
                    "Breastfeeding is good\n1)Disagree\n2)Agree",
                ),
                (
                    "inv_1__survey_2__question_3",
                    "What is your favourite color?\n1)Red\n2)Blue\n3)Yellow",
                ),
                (
                    "inv_1__survey_2__question_4",
                    "What is your favourite fruit?\n1)Banana\n2)Apple\n3)Pear",
                ),
                (
                    "inv_1__survey_2__question_5",
                    "What is your age?\n1)0-12\n2)13-30\n3)31+",
                ),
            ]
        )

    def test_get_validator_ids_from_ref(self):
        test_data_structure = self.inv_data["surveys"]["inv_1__survey_1"][
            "inv_1__survey_1__question_1"
        ]["validators"]
        result = get_validator_ids_from_ref(test_data_structure)
        self.assertEqual(result, ["agree", "disagree"])

    def test_check_message_response_numeric_valid(self):
        is_valid_answer, clean_answer, validation_error = check_answer(
            self.inv_data, "inv_1__survey_1", "inv_1__survey_1__question_1", "1"
        )
        self.assertTrue(is_valid_answer)
        self.assertEqual(clean_answer, "agree")
        self.assertFalse(validation_error)

    def test_check_message_response_numeric_not_valid(self):
        is_valid_answer, clean_answer, validation_error = check_answer(
            self.inv_data, "inv_1__survey_1", "inv_1__survey_1__question_1", "99"
        )
        self.assertFalse(is_valid_answer)
        self.assertTrue(clean_answer is None)
        self.assertEqual(validation_error, "Number given is not valid")

    def test_check_message_response_text(self):
        is_valid_answer, clean_answer, validation_error = check_answer(
            self.inv_data, "inv_1__survey_1", "inv_1__survey_1__question_1", "agree"
        )
        self.assertTrue(is_valid_answer)
        self.assertEqual(clean_answer, "agree")
        self.assertTrue(validation_error is None)

    def test_check_message_response_text_not_number(self):
        is_valid_answer, clean_answer, validation_error = check_answer(
            self.inv_data,
            "inv_1__survey_1",
            "inv_1__survey_1__question_5",
            "silly answer",
        )
        self.assertFalse(is_valid_answer)
        self.assertTrue(clean_answer is None)
        self.assertEqual(validation_error, "Invalid answer, please try again")

    def test_check_message_response_text_invalid_answer(self):
        is_valid_answer, clean_answer, validation_error = check_answer(
            self.inv_data,
            "inv_1__survey_1",
            "inv_1__survey_1__question_1",
            "silly answer",
        )
        self.assertFalse(is_valid_answer)
        self.assertTrue(clean_answer is None)
        self.assertTrue(validation_error, "Invalid answer, please try again")

    def test_get_next_question(self):
        question_id, question_text = get_next_question(
            self.inv_data, "inv_1__survey_1", ["inv_1__survey_1__question_1"]
        )
        self.assertIn(
            question_id,
            [
                "inv_1__survey_1__question_2",
                "inv_1__survey_1__question_3",
                "inv_1__survey_1__question_4",
                "inv_1__survey_1__question_5",
            ],
        )

    def test_get_next_question_mulitple_already_asked(self):
        question_id, question_text = get_next_question(
            self.inv_data,
            "inv_1__survey_1",
            [
                "inv_1__survey_1__question_1",
                "inv_1__survey_1__question_2",
                "inv_1__survey_1__question_3",
                "inv_1__survey_1__question_4",
            ],
        )
        self.assertEqual(question_id, "inv_1__survey_1__question_5")
