from app.services.llm import llm


def main():
    print(llm.generate("Reply with one short greeting."))


if __name__ == "__main__":
    main()
