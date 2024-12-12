from vm_translator import VMTranslator


def main():

    translator = VMTranslator("/Users/yoav/Downloads/BasicTest/BasicTest.vm")
    translator.translate()

if __name__ == "__main__":
    main()