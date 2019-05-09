#!/bin/bash

# trainPath="/home/yaok/software/cnn_prior/caffe/data/rbox/JPEGImages"
# validationPath="/home/yaok/software/cnn_prior/caffe/data/rbox/JPEGImages/test"
trainPath="/home/yaok/software/dataset/rbox_mask/resize_db/resize_img"
validationPath="/home/yaok/software/dataset/rbox_mask/resize_db/resize_img/test"

# positivePath="/home/yaok/Desktop/detect_datasets/positive"
# negativePath="/home/yaok/Desktop/detect_datasets/negative"
trainDirList=`ls $trainPath`


#for DirName in $trainDirList
#do
    cd $trainPath
    # 当前类别文件夹下图片总数
    dirNum=`ls -l|grep "^-"|wc -l`
    picList=`ls *.jpg`
    k=0
    for fileName in $picList
    do
	# echo $fileName
        fileNameArr[k]=$fileName
        k=$k+1
    done

    arr=($(seq 1 $dirNum))
    num=${#arr[*]}
    echo $arr
    echo $num
    # 需要转移到另外对应文件夹下的图片总数
    let filterNum=$num*1/4

    let i=0
    # 将所有生成的随机数保存进fileArr数组，作为要转移的图片的下标
    while(( i<=filterNum ));
    do
        res=${arr[$(($RANDOM%num))]}
        fileArr[i]=$res
        for((j=1;j<i;j++));
        do
        numJ=${fileArr[j]}
        if [[ $res == $numJ ]]; then
            unset fileArr[i]
            i=$i-1
            break
        fi
        done
        i=$i+1
    done

    cd $trainPath
#    mkdir $DirName
    for((indexNum=0;indexNum<$filterNum;indexNum++))
    do
       echo ${indexNum}
       echo ${fileNameArr[fileArr[indexNum]-1]}
       mv $trainPath/${fileNameArr[fileArr[indexNum]-1]} $validationPath/${fileNameArr[fileArr[indexNum]-1]}
    done

#done
