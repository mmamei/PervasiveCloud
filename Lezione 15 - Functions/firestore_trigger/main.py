
def hello_firestore(data, context):
    import json
    """ Triggered by a change to a Firestore document.
    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    trigger_resource = context.resource

    print('Function triggered by change to: %s' % trigger_resource)

    print('\nOld value:')
    print(json.dumps(data["oldValue"]))

    print('\nNew value:')
    print(json.dumps(data["value"]))

    person = trigger_resource.split('/')[-1]
    counter = data['value']['fields']['counter']['integerValue']
    print(f'{person}-->{counter}')