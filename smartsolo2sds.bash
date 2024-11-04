#######################################################
#Jonas Pätzel, 05.08.2024
#
#Script to sort mseed files into SDS data structure
#works with pyrocko squirrel
#
#IN : path where unsorted files are stored
#OUT : path where sds archive will be stored
#######################################################


IN=/media/joni/Elements/gunnuvher_july
OUT=/media/joni/Elements/gunnuvher_july/sds
cd $IN
echo "changing to: $(pwd)"
squirrel jackseis --add $IN --out-sds-path $OUT 
