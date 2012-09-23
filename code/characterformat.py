#!/usr/bin/evn python
#encoding=utf8

def TextUnicodeFormat(source_text_name, target_text_name, coding = "utf8"):
    '''
    Unicode the text, convert them to the format of "coding", default is "utf8"
    Output new format text
    '''

    # Open text file, if not exit, output error and exist
    import os, codecs

    if not os.path.exists(source_text_name):
        print "source text '%s'does not exist." % source_text_name
        print 'exit...'
        import sys
        sys.exit()

    source_text_name = os.path.abspath(source_text_name)
    target_text_name = os.path.abspath(target_text_name)
    rfd = open(source_text_name, "r")
    wfd = codecs.open(target_text_name, "w", encoding="utf-8")

    list_lines = rfd.readlines()
    length = len(list_lines)
    for i in range(length):
        format_text = SentenceUnicodeFormat(list_lines[i])
        if format_text != "":
            wfd.write(format_text[:-3] + "\n")

    rfd.close()
    wfd.close()

def SentenceUnicodeFormat(sentence, coding = "utf-8"):
    '''
    Process only sentence
    Return format sentence
    '''
    # Import character format processing package
    import chardet

    encoding = chardet.detect(sentence)['encoding']
    print encoding
    try:
        if encoding == "GB2312":
            encoding = "GBK"
        sentence = sentence.decode(encoding)
        print 'pass'
        sentence.encode(coding)
        #print sentence
        #print 'pass1'
        return sentence
    except:
        #print sentence
        print 'Encoding in sentence is inconsistent.'
        return ""

# Test
if __name__ == "__main__":
    source_text = "../corpus/Tang_poetry.txt"
    target_text = "../corpus/Tang_poetry_utf8.txt"

    TextUnicodeFormat(source_text, target_text)
