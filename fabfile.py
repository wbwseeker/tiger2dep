from __future__ import print_function

from fabric.api import local
from os import path

### globals
FABDIR = path.dirname(__file__)

# apply correction files
def correct(corpus, corrections, encoding):
	cmd = path.join(FABDIR,'apply-corrections.py')
	infile = path.abspath(path.expanduser(corpus))
	outfile = path.basename(infile)
	outfile = '%s.corrected.xml' % (path.splitext(outfile)[0] if outfile.endswith('.xml') else outfile)
	local('python %s %s %s %s %s' % (cmd,infile,outfile,corrections,encoding))
	return path.abspath(outfile)


# turn treebank into dependency treebank
def convert(corpus, manheads, source):
	cmd = path.join(FABDIR,'tigerxml2conll09.py')
	infile = path.abspath(path.expanduser(corpus))
	outfile = path.basename(infile)
	outfile = '%s.conll09' % (path.splitext(outfile)[0] if outfile.endswith('.xml') else outfile)
	local('python %s -m %s -i %s -o %s -d %s' % (cmd,manheads,infile,outfile,source))
	return outfile


def tiger(corpus):
	corrections = path.join(FABDIR,'corrections','corrections-tiger.pl')
	corrected = correct(corpus,corrections,'iso-8859-1')
	manheads = path.join(FABDIR,'corrections','manual_heads_tiger.pl')
	dependencies = convert(corrected,manheads,'tiger')
	print('Dependency version of TiGer stored in %s.' % dependencies)


def smultron(alpine, dvdman, economy, sophie):
	for corpus, name in zip([alpine,dvdman,economy,sophie],['alpine','dvdman','economy','sophie']):
		corrections = path.join(FABDIR,'corrections','corrections-%s.pl' % name)
		corrected = correct(corpus,corrections,'utf-8')
		manheads = path.join(FABDIR,'corrections','manual_heads_%s.pl' % name)
		dependencies = convert(corrected,manheads,'smultron')
		print('Dependency version of %s stored in %s.' % (name,dependencies))


def europarl(corpus):
	corrections = path.join(FABDIR,'corrections','corrections-europarl.pl')
	corrected = correct(corpus,corrections,'utf-8')
	manheads = path.join(FABDIR,'corrections','manual_heads_europarl.pl')
	dependencies = convert(corrected,manheads,'europarl')
	print('Dependency version of europarl707 stored in %s.' % dependencies)

