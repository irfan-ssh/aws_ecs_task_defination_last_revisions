import boto3

def get_last_revision_of_task_definitions(region_name):
    # Create ECS client with specified region
    ecs_client = boto3.client('ecs', region_name=region_name)

    try:
        # List all task definition families
        response = ecs_client.list_task_definition_families()

        last_revision_per_family = {}

        # Iterate through each task definition family
        for family_name in response['families']:
            # List all revisions of the family
            revisions_response = ecs_client.list_task_definitions(familyPrefix=family_name)

            # Extract the latest revision
            if revisions_response['taskDefinitionArns']:
                last_revision_per_family[family_name] = revisions_response['taskDefinitionArns'][-1]

        return last_revision_per_family

    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage:
region_name = "eu-central-1"  # Specify your AWS region here
last_revisions = get_last_revision_of_task_definitions(region_name)
if last_revisions:
    print("Last revision of each task definition family:")
    for family_name, last_revision in last_revisions.items():
        print(f"- Family: {family_name}, Last Revision: {last_revision}")
else:
    print("Failed to retrieve last revisions of task definitions.")
