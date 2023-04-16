def cfAspose(file_path):
    import os
    import aspose.slides as slides
    import aspose.pydrawing as drawing
    output_folder = 'Presentation'
    pres = slides.Presentation(file_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # Loop through slides
    for index in range(pres.slides.length):
        # Get reference of slide
        slide = pres.slides[index]
        size = drawing.Size(1920, 1080)

        # Save as PNG
        slide.get_thumbnail(size).save(os.path.join(output_folder, "{i}.png".format(i=index)),
                                       drawing.imaging.ImageFormat.png)
    return True
