import os

def main():
    for root, dirs, files in os.walk('.'):
        for f in files:
            path = os.path.join(root, f)
            try:
                with open(path, 'rb') as file:
                    content = file.read()
                if content.startswith(b'\xef\xbb\xbf'):
                    print(f'Fixed {path}')
                    with open(path, 'wb') as file:
                        file.write(content[3:])
            except Exception as e:
                pass

if __name__ == '__main__':
    main()
