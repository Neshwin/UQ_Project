
gen_list=pd.read_csv("gen_list.csv",index_col=0)
gen_dispatch_df=pd.DataFrame(0,columns=gen_list.index,index=demandSeries.index)
hydro_inflow=pd.read_csv("hydro_inflow.csv",index_col=0)
hydro_inflow1=pd.read_csv("hydro_inflow.csv",index_col=0)

for reg in regionList:
    # get mismatch splits
    reg_gen_list=gen_list[gen_list.region==reg]
    reg_gen_list = reg_gen_list.sort_values(by='dispatch_order')
    ds = splits['shortfall-' + reg]
    for idx in ds.index:
        demand=ds.at[idx]
        for gen in reg_gen_list.index:
            if demand>0.05:                

                    
                if idx.hour==0 and gen_list.at[gen,"generation_limit"]:
                    gen_limit_hydro=hydro_inflow.at[reg, str(idx.month)] / idx.days_in_month

                if gen_list.at[gen,"generation_limit"]:
                    # hydro_inflow=pd.read_csv("hydro_inflow.csv",index_col=0)
                    gen_limit=gen_limit_hydro
                else:
                    gen_limit=1000000000

                
                if idx==ds.index[0]:                
                    cap_lst=reg_gen_list.at[gen,'Capacity (GW)']
                    cap_avail=cap_lst
                    prev_gen=reg_gen_list.at[gen,'Capacity (GW)'] #remeber to add this
                    cap_avail=min(cap_lst,gen_limit)
                else:
                    cap_lst=reg_gen_list.at[gen,'Capacity (GW)']
                    rmp_rate=gen_list.at[gen,"ramp_rate"]/100
                    prev_gen=gen_dispatch_df.at[prev_ts,gen]
                    cap_avail=min(cap_lst,prev_gen+cap_lst*rmp_rate,gen_limit)
                
                # cap_avail=min(cap_lst,prev_gen*rmp_rate,gen_limit)
                    
                gen_dispatch=min(demand,cap_avail)
                demand-=gen_dispatch
                if gen_list.at[gen,"generation_limit"]:
                    # hydro_inflow=pd.read_csv("hydro_inflow.csv",index_col=0)
                    # hydro_inflow.at[reg,str(idx.month)]-=gen_dispatch #make sure its hourly reolution
                    gen_limit_hydro-=gen_dispatch
                gen_dispatch_df.at[idx,gen]=gen_dispatch
                prev_ts=idx
                
                
