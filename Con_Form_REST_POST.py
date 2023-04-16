def cfRestPost(file_path):
    import convertapi
    directory = 'Presentation'
    extension = '.png'
    convertapi.api_secret = 'BH8rIVQUZefbOjgn'
    convertapi.convert('png', {
        'File': file_path,
        'PngResolution': "1920x1080"
    }, from_format='pptx').save_files(directory)
    return True
