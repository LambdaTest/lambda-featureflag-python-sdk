from dataclasses import dataclass, asdict
import os
from amplitude_experiment import Experiment, User, LocalEvaluationConfig


class CustomError(Exception):
    pass


@dataclass
class UserProperties:
    org_id: str = None
    org_name: str = None
    username: str = None
    email: str = None
    plan: str = None
    hub_region: str = None
    user_status: str = None
    subscription_type: str = None
    infra_provider: str = None
    template_id: str = None


class FeatureFlag:
    def __init__(self, ):
        debug = bool(os.environ.get("LOCAL_EVALUATION_CONFIG_DEBUG")) or True
        server_url = os.environ.get("LOCAL_EVALUATION_CONFIG_SERVER_URL") or "https://api.lambdatest.com"
        flag_config_polling_interval_millis = (int(os.environ.get(
            "LOCAL_EVALUATION_CONFIG_POLL_INTERVAL")) or 120) * 1000
        flag_config_poller_request_timeout_millis = (int(os.environ.get(
            "LOCAL_EVALUATION_CONFIG_POLLER_REQUEST_TIMEOUT")) or 10) * 1000
        deploymentKey = os.environ.get("LOCAL_EVALUATION_DEPLOYMENT_KEY") or "server-jAqqJaX3l8PgNiJpcv9j20ywPzANQQFh"
        config = LocalEvaluationConfig(debug, server_url, flag_config_polling_interval_millis,
                                       flag_config_poller_request_timeout_millis)
        self.experiment = Experiment.initialize_local(deploymentKey, config)
        self.experiment.start()

    def fetch(self, flagName, user):
        if not isinstance(user, UserProperties):
            raise CustomError("invalid userProperties object has passed")
        expUser = User(user_properties=asdict(user))
        variants = self.experiment.evaluate(expUser, [flagName])
        return variants

    def GetFeatureFlagString(self, flagName, user):
        try:
            data = self.fetch(flagName, user)
            if data is not None and data.get(flagName) is not None:
                return data.get(flagName).value
            else:
                return ""
        except CustomError as e:
            print("An error occurred:", str(e))
            raise e

    def GetFeatureFlagBool(self, flagName, user):
        try:
            data = self.fetch(flagName, user)
            if data is not None:
                return bool(data.get(flagName).value)
            else:
                return False
        except CustomError as e:
            print("An error occurred:", str(e))
            raise e

    def GetFeatureFlagPayload(self, flagName, user):
        try:
            data = self.fetch(flagName, user)
            if data is not None:
                return data.get(flagName)
            else:
                return dict()
        except CustomError as e:
            print("An error occurred:", str(e))
            raise e
