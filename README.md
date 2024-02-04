# How to use this script

0.00. make sure you are using a computer with Internet access

0.42. if you're reading this on GitHub, download everything here (click on the `Code` button -> click on `Download ZIP`)

0.51. open File Explorer and navigate to the location you downloaded the ZIP file in the previous step

0.69. unzip the ZIP file (on Windows, right-click on the ZIP file, then click on "Extract All")

0.99. make sure you have Python and pip installed (get them at https://www.python.org/ if you don't)

1. open a console
    
    - if you're on Windows:
        1) press the Windows key (it's beside the `alt` key on your keyboard) and the R key at the same time
        2) type `cmd`
        3) press `enter`
    - if you're not just Google how to do it

2. change the working directory in your console

    in your console, run this (replace `<PATH>` with the path (location) of the unzipped file in step 0.69):
    ```
    cd <PATH>
    ```

    FOR EXAMPLE, if the path of your unzipped file was `C:\Users\username\Downloads\mods-downloader-main`, you'd run
    ```
    cd C:\Users\username\Downloads\mods-downloader-main
    ```

3. install dependencies

    run this command in your console (copy-paste it):
    ```
    py -m pip install -r requirements.txt
    ```

4. run the script

    1) double-click on `download.py`

        **OR**

    2) run this command in your console:

        ```
        python download.py
        ```
    
    when it prompts you, type `y` and press `Enter`

After running the script, all the JAR files of the mods should be in the folder `OUTPUT_MODS`.