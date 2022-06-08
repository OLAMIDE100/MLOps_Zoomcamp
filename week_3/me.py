from prefect.client import Client

flow_id = "mide_flow"

client = Client()
client.graphql(
    """
    mutation {
    delete_flow(input: {flow_id: "%s"}) {
        success
    }
    }
    """ % flow_id
)