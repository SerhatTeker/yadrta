from uuid import UUID

from django.urls import reverse


def user_id_to_hex(uuid: str) -> str:
    """Turn uuid4 with dashes to hex:
    From    :  8791f25b-d4ca-4f10-8f60-407a507edefe
    To      :  8791f25bd4ca4f108f60407a507edefe

    :param uuid: uuid string with dashes
    :type uuid: str

    :returns: str - hex of uuid
    """

    return UUID(uuid).hex


class APIClientUtils:
    def set_url(self):
        self.url = reverse(f"{self.model}-list")

    def set_url_list(self):
        self.url_list = reverse(f"{self.model}-list")

    def get_model_url_list(self):
        return reverse(f"{self.model}-list")

    def _set_payload(self, name=None, created_by=None):
        if name and created_by is None:
            name = self.tag_data.get("name")
            created_by = self.user.pk

        payload = {"name": name, "created_by": created_by}

        return payload

    def set_payload(self):
        """Default payload for cls"""
        # payload = {"name": self.tag_data.get("name"), "created_by": self.user.pk}
        name = self.tag_data.get("name")
        created_by = self.user.pk

        return self._set_payload(name=name, created_by=created_by)

    def client_get(self, url=None):
        if not url:
            url = self.url

        return self.client.get(url)

    def client_post(self, url=None, payload=None):
        response = None

        if url and payload is None:
            url = self.url
            payload = self.payload

        response = self.client.post(self.url, self.payload)

        return response

    def get_obj_url(self, object_pk):
        """Use self.tag_data if exists otherwise use self.tag"""
        return reverse(f"{self.model}-detail", kwargs={"pk": object_pk})
