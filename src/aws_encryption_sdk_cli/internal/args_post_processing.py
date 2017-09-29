# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""Arguments post-processors for known master key providers."""
import copy
from typing import Dict, List, Text, Union  # noqa pylint: disable=unused-import

import botocore.session

from aws_encryption_sdk_cli.exceptions import BadUserArgumentError


def nop_config(kwargs):
    # type: (Dict[str, List[Union[Text, str]]]) -> Dict[str, List[Union[Text, str]]]
    """Stand-in NOP post-processor. Does not modify kwargs.

    :param dict kwargs: Named parameters collected from CLI arguments
    :returns: Unmodified kwargs
    :rtype: dict
    """
    return copy.deepcopy(kwargs)


def kms_master_key_provider(kwargs):
    # type: (Dict[str, List[Union[Text, str]]]) -> Dict[str, List[Union[Text, str]]]
    """Apply post-processing to transform KMSMasterKeyProvider-specific arguments from CLI arguments
    to class parameters.

    :param dict kwargs: Named parameters collected from CLI arguments
    :returns: Updated kwargs
    :rtype: dict
    """
    kwargs = copy.deepcopy(kwargs)
    try:
        profile_name = kwargs.pop('profile')
        if len(profile_name) != 1:
            raise BadUserArgumentError(
                'Only one profile may be specified per master key provider configuration. {} provided.'.format(
                    len(profile_name)
                )
            )
        kwargs['botocore_session'] = botocore.session.Session(profile=profile_name[0])
    except KeyError:
        pass
    try:
        region_name = kwargs.pop('region')
        kwargs['region_names'] = region_name
    except KeyError:
        pass
    return kwargs
