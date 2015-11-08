library(readr)
data <- "R.dict"

#d <- read_csv(data)
d <- read.table(file=data,
                header=F,
                sep="\t",
                stringsAsFactors=F)

colnames(d) <- c("登记证号",
                 "登记名称",
                 "公司名称",
                 "毒性",
                 "有效成分及含量",
                 "有效期起始日",
                 "有效期终止日",
                 "剂型",
                 "登记作物名称",
                 "防治对象名称",
                 "用药量",
                 "施用方法",
                 "英文剂型",
                 "英文有效成分及含量")

mdata <- "M.dict"
mdict <- read.table(file=mdata,
                    header=F,
                    fileEncoding="GB18030",
                    sep="\t",
                    stringsAsFactors=F)
colnames(mdict) <- c("zh", "en")

tcol <- d$有效成分及含量
list1 <- strsplit(tcol, "、")
lapply(list1, function(x){
    list2 <- strsplit(x, " ")
    lapply(list2, function(y){

    })

})


formdata <- "formulation.txt"
fdict <- read.table(file=formdata,
                    header=F,
                    fileEncoding="GB18030",
                    sep="\t",
                    stringsAsFactors=F)

colnames(mdict) <- c("zh", "en")

write.table(cdict,
            file="cdict",
            row.names=F,
            col.names=T,
            quote=F,
            sep="\t")





write.table(mdict,
            file="mdict",
            fileEncoding="GB18030",
            row.names=F,
            col.names=T,
            quote=F,
            sep="\t")


write.table(d,
            file="rrr",
            row.names=F,
            col.names=T,
            fileEncoding="GB18030",
            quote=F,
            sep="\t")
