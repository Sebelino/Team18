
"""pygtk is now installed on your machine.

Local configuration files were successfully updated."""

import os, os.path, re, sys
import distutils.sysconfig
import distutils.file_util
import distutils.errors

pkgconfig_file = os.path.normpath(
    os.path.join(sys.prefix,
                 'lib/pkgconfig/pygtk-2.0.pc'))

prefix_pattern=re.compile("^prefix=.*")
exec_pattern=re.compile("^exec\s.*")
codegendir_pattern=re.compile("^codegendir=.*")
version_pattern=re.compile("Version: ([0-9]+\.[0-9]+\.[0-9]+)")

def replace_prefix(s):
    if prefix_pattern.match(s):
        s='prefix='+sys.prefix.replace("\\","/")+'\n'
    if exec_pattern.match(s):
        s=('exec '+sys.prefix+'\\python.exe '+
           '$codegendir/codegen.py \"$@\"\n').replace("\\","/")
    if codegendir_pattern.match(s):
        s=('codegendir='
           +distutils.sysconfig.get_python_lib().replace("\\","/")+
           '/gtk-2.0/codegen' + '\n')
    return s

def get_doc_url(pkgconfig_file, base_url):
    try:
        f = open(pkgconfig_file).read()
        ver = version_pattern.search(f).groups()[0]
        majv,minv,micv = ver.split('.')
        doc_url = "%s/%s.%s/" % (base_url,majv,minv)
    except:
        doc_url = base_url + "/stable/"
    return doc_url

# TODO : Check that shortcuts are created system-wide when the user
# has admin rights (hint: see pywin32 postinstall)
def create_shortcuts():
    progs_folder= get_special_folder_path("CSIDL_COMMON_PROGRAMS")
    site_packages_dir = os.path.join(sys.prefix , 'lib','site-packages')
   
    pygtk_shortcuts = os.path.join(progs_folder, 'PyGTK')
    if not os.path.isdir(pygtk_shortcuts):
        os.mkdir(pygtk_shortcuts)

    # link to specific documentation version by parsing the
    # pkgconfig file
    doc_url = get_doc_url(pkgconfig_file,
                          "http://library.gnome.org/devel/pygtk")
    pygtk_doc_link=os.path.join(pygtk_shortcuts,
                                    'PyGTK Documentation.lnk')
    if os.path.isfile(pygtk_doc_link):   
        os.remove(pygtk_doc_link)
    create_shortcut(doc_url,'PyGTK Documentation',pygtk_doc_link)
   
    homepage_link = os.path.join(pygtk_shortcuts,
                                 "PyGTK Home.lnk")
    if os.path.isfile(homepage_link):   
        os.remove(homepage_link)
    create_shortcut("http://www.pygtk.org",'PyGTK Homepage',homepage_link)

def remove_shortcuts():
    pygtk_shortcuts = os.path.join(
        get_special_folder_path('CSIDL_COMMON_PROGRAMS'), 'PyGTK')
    os.remove(os.path.join(pygtk_shortcuts,'PyGTK Documentation.lnk'))
    os.remove(os.path.join(pygtk_shortcuts,'PyGTK Home.lnk'))
    try:
        os.rmdir(pygtk_shortcuts)
    except OSError, e:
        # Directory is not empty, so leave it like that !
        pass

if len(sys.argv) == 2:
    if sys.argv[1] == "-install":
        # fixup the pkgconfig file
        lines=open(pkgconfig_file).readlines()
        open(pkgconfig_file, 'w').writelines(map(replace_prefix,lines))
        # TODO: Add an installer option for shortcut creation 
        create_shortcuts()
        print __doc__
    elif sys.argv[1] == "-remove":
        remove_shortcuts()
