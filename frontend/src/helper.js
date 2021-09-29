
function dateRange(dateDebut,dateFin){
    const data=[];
    
    while((dateDebut[0] !==dateFin[0])&&(dateDebut[1] !==dateFin[1])){
        data.push(''+dateDebut[0]+'-'+dateDebut[1]+'-'+'01')
        dateDebut=dateDiff(dateDebut,1)
        console.log(data)
    }
    data.push(''+dateDebut[0]+'-'+dateDebut[1]+'-'+'01')

    return(data)
}

function dateDiff([y,m],delta){
    if (delta>0){
        m=m+delta
        var x=Math.floor(m/12)
        var mod= m%12
        if (mod==0){mod=12}
        return [y+x,mod]
    
    }else{
        m=m+delta
        if (m<0){
            y=y-1
            var x=Math.floor(-m/12)
            var mod= -m%12
            return [y-x,12-mod]
        }else{
            return[y,m]
        }
    }
   
}


export  {
    dateDiff,
    dateRange,
  }
