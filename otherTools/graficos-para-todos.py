
import os

from fabric.api import * 


import files



class pythonFile():
    """dedicated to the files"""

    filename= ""
    basename= ""
    dotfile= ""
    graph= ""
    dest= "./graphs"

    def set_filename(self,filename):
        self.filename = filename

    def get_basename(self,filename):
        #- guess the basename
        file = os.path.basename(filename)
        basename = file.split(".")[0]
        if self.basename == "":
            self.basename = basename
        return basename

    def make_dotfile(self):
        """ create the dotfile in destination"""
        self.dotfile = self.basename + ".dot"
        local("cat {file} | {parser} > {dest}/{destfile} ".format(
            file = self.filename,
            parser = "otherTools/construct_call_graph.py",
            dest = self.dest,
            destfile = self.dotfile
        ))

    def make_graph(self, kind="png"):
        """create a graphic using a dotfile"""
        local("dot -T{kind} {dest}/{dotfile} > {dest}/{destfile}".format(
            kind = kind,
            dest = self.dest,
            dotfile = self.dotfile,
            destfile = self.basename + ".png"
        ))



def create_graphs(filenames=files.files):
    """create graphs for all files"""
    python_files = []
    for filename in filenames:
        nufil = pythonFile()
        nufil.set_filename(filename)
        basename = nufil.get_basename(filename)
        python_files.append(nufil)

    for pyfile in python_files:
        pyfile.make_dotfile()

    for pyfile in python_files:
        pyfile.make_graph()


if __name__ == "__main__":
    create_graphs()
