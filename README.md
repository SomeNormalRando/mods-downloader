# How to use this script

0.00. make sure you are using a computer with Internet access

0.20. if you're reading this on GitHub, download everything here (click on the `Code` button -> click on `Download ZIP`)

0.40. open File Explorer and navigate to the location you downloaded the ZIP file in the previous step

0.60. unzip the ZIP file (on Windows, right-click on the ZIP file, then click on "Extract All")

0.69. open the unzipped folder. there likely is another folder with the same name inside it. open it and you should see the same files you saw on GitHub. copy the path (location) of the second folder (the one containing the files)

0.99. make sure you have Python and pip installed (get them at https://www.python.org/ if you don't)

1. open a console
	- if you're on Windows:
		1) press the Windows key (it's beside the `alt` key on your keyboard) and the R key at the same time
		2) type `cmd`
		3) press `enter`
	- if you're not just Google how to do it

2. change the working directory in your console

	In your console, run `cd <folder path>` (replace *`<folder path>`* with the path (location) of the unzipped folder in step 0.69)

	FOR EXAMPLE, if the path of your unzipped folder was `C:\Users\username\Downloads\mods-downloader-main\mods-downloader-main`, you'd run
	```
	cd C:\Users\username\Downloads\mods-downloader-main\mods-downloader-main
	```

	**After running `cd`, the text on the left side of your console should change to* `<folder path>`*. It should look something like this:*
	```
	C:\Users\username>cd C:\test\mods-downloader-main\mods-downloader-main
	C:\test\mods-downloader-main\mods-downloader-main>
	```
	*If it doesn't and you're on Windows, your* `<folder path>` *is likely in another drive. If that's the case, run `cd /D` instead of `cd`.* 

3. install dependencies

	run this command in your console (copy-paste it):
	```
	py -m pip install -r requirements.txt
	```

4. run the script

	1) double-click on `download.py` (in the folder in step 0.69)

		**OR**

	2) run this command in your console:

		```
		py download.py
		```

	when it prompts you, type `y` and press `Enter`

After running the script, all the JAR files of the mods should be in the folder `OUTPUT_MODS`.