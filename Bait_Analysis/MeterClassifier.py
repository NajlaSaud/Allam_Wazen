from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from pathlib import Path
from dotenv import load_dotenv
import json
import os

# Define path to config.json
config_path = Path(__file__).parent / "config.json"

# Load the JSON file of keys
with open(config_path, "r") as file:
    var = json.load(file)

# load_dotenv(dotenv_path="variables.env")
credentials = {
    "url": "https://eu-de.ml.cloud.ibm.com",
    "apikey": var.get("IBM_API_KEY")
}
api_url = credentials['url']
api_key = credentials['apikey']
# print(f"api_key: {api_key}")
project_id = var.get("IBM_PROJECT_ID")
client = APIClient(credentials)
client.set.default_project(project_id)

# token = var.get("WAZEN_PROJECT_ID")
# credentials = Credentials(
#     token=token,
#     url="https://ai.deem.sa",
#     instance_id="openshift",
#     version="5.0"
# )

# client = APIClient(credentials)
# project_id = var.get("WAZEN_PROJECT_ID")
# client.set.default_project(project_id)

gen_parms_override = gen_parms = {
    GenParams.DECODING_METHOD: DecodingMethods.SAMPLE,
    GenParams.MAX_NEW_TOKENS: 50,
    GenParams.TEMPERATURE: 0,
    GenParams.RANDOM_SEED: 1
}


class MeterClassifier:

    def get_credentials(self):
        return {
            "url": "https://eu-de.ml.cloud.ibm.com",
            "apikey": os.getenv("IBM_API_KEY")
        }

    def get_params(self):
        generate_params = {
            GenParams.MAX_NEW_TOKENS: 20,
            GenParams.DECODING_METHOD: 'greedy',
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.TRUNCATE_INPUT_TOKENS: 3975,
            GenParams.TEMPERATURE: 0,
            GenParams.RANDOM_SEED: 0
        }
        return generate_params

    def get_tuned_model(self):
        deployment_id = var.get("DEPLOYMENT_ID")
        tuned_model = ModelInference(
            deployment_id=deployment_id,
            params=self.get_params(),
            api_client=client
        )
        return tuned_model

    def generate_meter(self, poem):
        tuned_model = self.get_tuned_model()
        meter = tuned_model.generate_text(prompt=poem, params=gen_parms_override)
        return meter


def main():
    # create object from the class
    classifier = MeterClassifier()

    bait = "مالي سوى دعوات قلب خاشع"
    poem = "ظلت بها تنطوي على كبد نضيجة فوق خلبها يدها"
    meter = classifier.generate_meter(poem.strip())

    # print sentence
    print(meter)


if __name__ == "__main__":
    main()
