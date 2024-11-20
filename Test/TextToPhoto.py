from zhipuai import ZhipuAI


class TextToPhoto:
    def __init__(self, prompt):
        self.prompt = prompt

    def generate(self):
        if self.prompt:
            client = ZhipuAI(api_key="f962cb6d0919af506ed9c906806c0c3a.lKBewKeFDhZC8jK6")
            response = client.images.generations(
                model="cogView-3-plus",
                prompt=self.prompt,
                size="1440x720"
            )
            return response.data[0].url
