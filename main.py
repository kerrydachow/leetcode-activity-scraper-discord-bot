from models.client import Client


def main():
    client = Client()
    client.add_user("kerrydachow")
    client.add_user("nickfurk")
    client.execute_request(1)
    client.execute_request(2)


if __name__ == "__main__":
    main()
