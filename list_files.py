import os
import open_embl as oe
import matplotlib.pyplot as plt
import sys

def return_lists(path,prefix,extension):
    initial_list = []
    for element in os.listdir(path):
        if element.endswith(extension):
            if prefix in element:
                 initial_list.append(element)
    initial_list = sorted(initial_list)
    return initial_list


def consistent_list(path,sample,background,cut):
    # sample is the name of the sample file --- complete
    list_sample = return_lists(path,sample,'.dat')
    list_background = return_lists(path,background,'.dat')
    list_sample = list_sample[0:cut]
    list_background = list_background[0:cut]
    return list_sample,list_background


def subtract_intensities(path,file_sample,file_background):
      q_s,i_sample,e_s = oe.give_columns('%s%s'%(path,file_sample))
      q_b,i_background,e_b = oe.give_columns('%s%s'%(path,file_background))
      if len(i_sample) == len(i_background):
          
          i_subtracted = map(float.__sub__, i_sample, i_background)
          return q_s,i_subtracted,e_s


def input_file_writer(q,i_subtracted,error,file_sample,file_background):
    
    name_subtracted = '%s_minus_%s.dat'%(file_sample.split('.dat')[0],file_background.split('.dat')[0])
    file_name = open(name_subtracted,'w')
    file_name.write('# file sample: %s subtracted from file background: %s\n'%(file_sample,file_background))
    file_name.write('# q(1/A)      	Intensity      	Error\n')
    for i,element in enumerate(q):
        file_name.write('%s\t'%q[i])
        file_name.write('%s\t'%i_subtracted[i])
        file_name.write('%s\n'%error[i])
    file_name.close()
    return name_subtracted 
    
    
def auto_rg_results_in1file(text_rg):

    name_autorg_file = 'all_results_rg.dat'
    
    file_open = open(name_autorg_file,'a')
    file_open.write(str(text_rg) + '\n')
    file_open.close()

def execute_rg(file_subtracted):
    os.system('autorg %s > temp_rg.txt'%file_subtracted)
    file_open = open('temp_rg.txt','r').readlines()
    auto_rg_results_in1file(file_open)
    #print file_open
    return file_open

def extrac_autorg_columns(file_results):

    file_open = open(file_results,'r').readlines()
    rg_list = []
    intensity_list = []
    quality_list = []
    
    for item in file_open:
        if 'Rg   =' in item:
            list_rg = item.split(',')
            rg_list.append(float(list_rg[0].split('Rg   =')[1].split('+/-')[0]))
            intensity_list.append(float(list_rg[1].split('I(0) =   ')[1].split('+/-')[0]))
            quality_list.append(float(list_rg[3].split('Quality: ')[1].split('%')[0]))

    return rg_list, intensity_list, quality_list


def auto_rg_results_writer(rgs, intensities, qualities):

    name_all_rg = 'results_all_rg.txt'#%(file_sample.split('.dat')[0],file_background.split('.dat')[0])
    file_name = open(name_all_rg,'w')
    #file_name.write('# file sample: %s subtracted from file background: %s\n'%(file_sample,file_background))
    file_name.write('Radius of gyration(Rg)\tIntensity(I(0))\tQuality Factor (%)\n')
    for i,element in enumerate(rgs):
        file_name.write('%s\t'%rgs[i])
        file_name.write('%s\t\t\t'%intensities[i])
        file_name.write('%s\n'%qualities[i])
    file_name.close()

    
def plot_rg_evolution(list_plot):
    plt.plot(list_plot,'o-')
    plt.ylabel('Radius of gyration')
    plt.xlabel('File number')
    plt.show()


def subtract_all(path,prefix_sample,prefix_background):

    if os.path.exists('all_results_rg.dat'):
        os.system('rm all_results_rg.dat')

    
    list_sample,list_background = consistent_list(path,prefix_sample,prefix_background,190)

    for i,element in enumerate(list_sample):

        file_sample = list_sample[i]
        file_background = list_background[i]
        q_s,i_subtracted,e_s =  subtract_intensities(path,file_sample,file_background)
        name_subtracted = input_file_writer(q_s,i_subtracted,e_s,file_sample,file_background)
        execute_rg(name_subtracted)

    rgs, intensities, qualities = extrac_autorg_columns('all_results_rg.dat')
    auto_rg_results_writer(rgs, intensities, qualities)
    os.system('rm all_results_rg.dat')

    plot_rg_evolution(rgs)

curr_directory = '%s/'%os.getcwd()
   
path = curr_directory
prefix_sample = 'img_0009_'
prefix_background = 'img_0008_'




if __name__ == '__main__':

    print sys.argv

    if len(sys.argv) == 3:

        print 'found'

        prefix_sample = sys.argv[1]
        prefix_background = sys.argv[2]

    subtract_all(path,prefix_sample,prefix_background)

