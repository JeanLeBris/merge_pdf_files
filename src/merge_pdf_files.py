import argparse
import os
import sys
import subprocess
import shutil

def merge_pdf_files(input_dir, output_file):
    project_src = os.path.split(os.path.split(sys.argv[0])[0])[0]
    temp_dir = os.path.join(project_src, "temp")
    template_file = os.path.join(project_src, "template", "template.tex")

    os.makedirs(temp_dir)

    content = ""
    with open(template_file, "r") as f:
        content = f.read()
    
    pdf_files = [os.path.join(input_dir, f).replace("\\", "/") for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and f.split('.')[-1] == "pdf"]
    tex_calls = ["\\includepdf{" + f + "}" for f in pdf_files]
    tex_text = "\n".join(tex_calls)
    
    content = content.replace("<!-- PUT CONTENT HERE -->", tex_text)

    with open(os.path.join(temp_dir, "document.tex"), "w") as f:
        f.write(content)
    
    print(temp_dir)
    subprocess.run(f"powershell; cd {temp_dir}; pdflatex document.tex", shell=True)

    shutil.copyfile(os.path.join(temp_dir, "document.pdf"), output_file)
    
    # print(content)

    # os.rmdir(temp_dir)
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    INPUT = None
    INPUT_VERSION = -1
    OUTPUT = None
    OUTPUT_VERSION = -1
    parser = argparse.ArgumentParser(prog="Merger", description="Merge multiple PDF files into a single multipages PDF file")
    parser.add_argument('-i', '--input', required=True, help="input directory")
    parser.add_argument('-o', '--output', required=True, help="output file")
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        pass
    else:
        print("input directory doesn't exist")
        quit()

    if os.path.isfile(args.output):
        print("output file exists already")
        quit()
    elif os.path.isdir(args.output):
        print("output file entered is a directory")
        quit()
    elif os.path.isdir(os.path.split(args.output)[0]):
        pass
    else:
        print("output file name error")
        quit()
    
    merge_pdf_files(args.input, args.output)