import json


# fileLength, sleepLength ,recognitionLanguage, translationLanguage, display, recordKey, openChatKey, closeChatKey
class Parser:
    fileName = ""

    def __init__(self, fileName="Settings"):
        self.fileName = fileName + ".json"

    def Parse(self, fileLength, sleepLength, recognitionLanguage, translationLanguage, recordKey, openChatKey,
              closeChatKey):
        jString = {
            "FileLength": fileLength,
            "SleepLength": sleepLength,
            "RecognitionLanguage": recognitionLanguage,
            "TranslationLanguage": translationLanguage,
            "RecordKey": recordKey,
            "OpenChatKey": openChatKey,
            "CloseChatKey": closeChatKey
        }
        parse = json.dumps(jString)
        self.Save(parse)

    def Save(self, parseObject):
        with open(self.fileName, 'w') as outfile:
            outfile.write(parseObject)

    def Load(self, spBoxRecording, spBoxSleepTime, comBoxLanguage, comBoxTranslation, keySequenceRecord, keySequenceOpenChat, keySqeuenceCloseChat):
        with open(self.fileName) as infile:
            jsonData = json.load(infile)
        spBoxRecording.setValue(jsonData["FileLength"])
        spBoxSleepTime.setValue(jsonData["SleepLength"])
        comBoxLanguage.setCurrentIndex(comBoxLanguage.findText(jsonData["RecognitionLanguage"]))
        comBoxTranslation.setCurrentIndex(comBoxTranslation.findText(jsonData["TranslationLanguage"]))
        keySequenceRecord.setKeySequence(jsonData["RecordKey"])
        keySequenceOpenChat.setKeySequence(jsonData["OpenChatKey"])
        keySqeuenceCloseChat.setKeySequence(jsonData["CloseChatKey"])
