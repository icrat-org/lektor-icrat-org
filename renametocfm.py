# coding=utf-8
import os
import io
import chardet
import codecs


TRANSFORM_ENCODING = 'utf-8-sig'

def main():
    path = "build/"
    count = 1

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".html") or file.endswith(".cfm"):
                original_file = os.path.join(root, file)
                num_bytes = os.path.getsize(original_file)
                file_contents = None
                encoding = None
                with open(original_file, 'rb') as fp:
                    b = fp.read(num_bytes)
                    result = chardet.detect(b)
                    if result and 'encoding' not in result:
                        print('could not detect encoding', result['encoding'], original_file)
                        continue
                    
                    if result['encoding'].lower() != TRANSFORM_ENCODING:
                        file_contents = b
                        encoding = result['encoding'].lower()
                        print("encoded with {} encoding to {}".format(encoding, TRANSFORM_ENCODING), original_file)
                    else:
                        print("encoded with " + TRANSFORM_ENCODING, original_file)

                if file_contents:
                    content = file_contents.decode(encoding).encode(TRANSFORM_ENCODING)
                    with open(original_file, "wb") as fp:
                        fp.write(content)
                    with io.open(original_file, 'r', encoding=TRANSFORM_ENCODING) as fp:
                        file_contents = fp.read()
                    content = file_contents.replace(u'Ă¨', u'è').replace(u'รง', u'ç')
                    with io.open(original_file, "w", encoding=TRANSFORM_ENCODING) as fp:
                        fp.write(content)
                    
                if file.endswith(".html"):
                    os.rename(os.path.join(root, file), os.path.join(root, file[:-1*len(".html")] + ".cfm"))
                

if __name__ == '__main__':
    main()
