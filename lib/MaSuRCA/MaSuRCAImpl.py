# -*- coding: utf-8 -*-
#BEGIN_HEADER
# The header block is where all import statments should live
import os
import json
import time
from MaSuRCA.core.masurca_assembler import MaSuRCA_Assembler
#END_HEADER


class kb_MaSuRCA:
    '''
    Module Name:
    kb_MaSuRCA

    Module Description:
    Name of module: MaSuRCA

This KBase module wraps the genome assembly software MaSuRCA(Maryland Super-Read Celera Assembler).
MaSuRCA 3.2.9


References:
https://academic.oup.com/bioinformatics/article/29/21/2669/195975/The-MaSuRCA-genome-assembler
https://academic.oup.com/bioinformatics/article-lookup/doi/10.1093/bioinformatics/btt476
ftp://ftp.genome.umd.edu/pub/MaSuRCA/latest/
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "1.1.1"
    GIT_URL = "https://github.com/kbaseapps/kb_MaSuRCA.git"
    GIT_COMMIT_HASH = "f5315c14b5d0759de80a8f7a71a1de2c4cf27fda"

    #BEGIN_CLASS_HEADER
    # Class variables and functions can be defined in this block

    def log(self, message, prefix_newline=False):
        print(('\n' if prefix_newline else '') +
              str(time.time()) + ': ' + str(message))
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR

        # Any configuration parameters that are important should be parsed and
        # saved in the constructor.
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        #END_CONSTRUCTOR
        pass


    def run_masurca_assembler(self, ctx, params):
        """
        Definition of run_masurca_assembler
        :param params: instance of type "masurcaAssemblerParams" (Arguments
           for run_masurca_assembler *******for creating the sr_config.txt
           file******* 1. DATA consisting of 5 fields: 1)two_letter_prefix
           2)mean 3)stdev 4)fastq(.gz)_fwd_reads 5)fastq(.gz)_rev_reads.
           e.g., PE= pe 180 20  /FULL_PATH/frag_1.fastq 
           /FULL_PATH/frag_2.fastq JUMP= sh 3600 200 
           /FULL_PATH/short_1.fastq  /FULL_PATH/short_2.fastq #pacbio OR
           nanopore reads must be in a single fasta or fastq file with
           absolute path, can be gzipped #if you have both types of reads
           supply them both as NANOPORE type PACBIO=/FULL_PATH/pacbio.fa
           NANOPORE=/FULL_PATH/nanopore.fa OTHER=/FULL_PATH/file.frg 2.
           PARAMETERS string graph_kmer_size - the k-mer size for deBruijn
           graph values between 25 and 127 are supported, 'auto' will compute
           the optimal size based on the read data and GC content bool
           use_linking_mates - set this to 1 for all Illumina-only
           assemblies; set this to 1 if you have less than 20x long reads
           (454, Sanger, Pacbio) and less than 50x CLONE coverage by
           Illumina, Sanger or 454 mate pairs; otherwise keep at 0 string
           dna_source - indicate 'bacteria' or 'other organisms' for setting
           limit_jump_coverage and cgwErrorRate values int
           limit_jump_coverage - this parameter is useful if you have too
           many Illumina jumping library mates. Typically set it to 60 for
           bacteria and 300 for the other organisms CA_PARAMETERS: these are
           the additional parameters to Celera Assembler.  do not worry about
           performance, number or processors or batch sizes -- these are
           computed automatically. float cgwErrorRate=0.15 - set
           cgwErrorRate=0.25 for bacteria and 0.1<=cgwErrorRate<=0.15 for
           other organisms. int kmer_count_threshold - minimum count k-mers
           used in error correction 1 means all k-mers are used.  one can
           increase to 2 if Illumina coverage >100 bool close_gaps - whether
           to attempt to close gaps in scaffolds with Illumina data (1) or
           not (0) int num_threads - auto-detected number of cpus to use,
           mandatory int jf_size  - this is mandatory jellyfish hash size --
           a safe value is estimated_genome_size*estimated_coverage (e.g.,
           2000000000) bool SOAP_ASSEMBLY - set this to 1 to use SOAPdenovo
           contigging/scaffolding module.  Assembly will be worse but will
           run faster. Useful for very large (>5Gbp) genomes bool
           do_homopolymer_trim - specifies if we do (1) or do not (0) want to
           trim long runs of homopolymers string workspace_name - the name of
           the workspace from which to take input and store output. string
           output_contigset_name - the name of the output contigset
           list<paired_readsParams> read_libraries - Illumina
           PairedEndLibrary files to assemble @optional jump_libraries
           @optional pacbio_reads @optional other_frg_file @optional
           graph_kmer_size @optional use_linking_mates @optional dna_source
           @optional kmer_count_threshold @optional close_gaps @optional
           soap_assembly @optional do_homopolymer_trim) -> structure:
           parameter "workspace_name" of String, parameter "num_threads" of
           Long, parameter "jf_size" of Long, parameter "reads_libraries" of
           list of type "paired_readsParams" (parameter groups) -> structure:
           parameter "pe_id" of type "obj_ref" (An X/Y/Z style KBase object
           reference), parameter "pe_prefix" of String, parameter "pe_mean"
           of Long, parameter "pe_stdev" of Long, parameter "jump_libraries"
           of list of type "jump_readsParams" -> structure: parameter "jp_id"
           of type "obj_ref" (An X/Y/Z style KBase object reference),
           parameter "jp_prefix" of String, parameter "jp_mean" of Long,
           parameter "jp_stdev" of Long, parameter "pacbio_reads" of type
           "obj_ref" (An X/Y/Z style KBase object reference), parameter
           "nanopore_reads" of type "obj_ref" (An X/Y/Z style KBase object
           reference), parameter "other_frg_file" of String, parameter
           "graph_kmer_size" of String, parameter "use_linking_mates" of type
           "bool" (A boolean - 0 for false, 1 for true. @range (0, 1)),
           parameter "dna_source" of String, parameter "kmer_count_threshold"
           of Long, parameter "close_gaps" of type "bool" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter "soap_assembly" of
           type "bool" (A boolean - 0 for false, 1 for true. @range (0, 1)),
           parameter "do_homopolymer_trim" of type "bool" (A boolean - 0 for
           false, 1 for true. @range (0, 1)), parameter
           "output_contigset_name" of String, parameter "create_report" of
           type "bool" (A boolean - 0 for false, 1 for true. @range (0, 1))
        :returns: instance of type "masurcaResults" (Output parameter items
           for run_masurca_assembler report_name - the name of the
           KBaseReport.Report workspace object. report_ref - the workspace
           reference of the report.) -> structure: parameter "report_name" of
           String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_masurca_assembler
        self.log('Running run_masurca_assembler with params:\n{}'.format(
                 json.dumps(params, indent=1)))

        for key, value in params.items():
            if isinstance(value, str):
                params[key] = value.strip()

        masurca_assembler = MaSuRCA_Assembler(self.config, ctx.provenance())

        output = masurca_assembler.run_masurca_assembler(params)
        #END run_masurca_assembler

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_masurca_assembler return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
