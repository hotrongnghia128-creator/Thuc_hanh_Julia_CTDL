root=dirname(dirname(@__DIR__))
include(joinpath(root,"TH_2026_10_09_Pluto.jl"))
@assert du_lieu === nothing && bao_cao === nothing
mktempdir() do stage
    cp(joinpath(root,"TH_2026_10_09_Loi_giai.jl"),joinpath(stage,"TH_2026_10_09_Sinh_vien.jl"))
    mkpath(joinpath(stage,"data","MINI001"))
    for name in ("don_hang.csv","ban_do.csv")
        cp(joinpath(@__DIR__,"data","MINI001",name),joinpath(stage,"data","MINI001",name))
    end
    text=read(joinpath(root,"TH_2026_10_09_Pluto.jl"),String)
    text=replace(text,"READ_DATA = false"=>"READ_DATA = true","RUN_APP = false"=>"RUN_APP = true")
    write(joinpath(stage,"notebook.jl"),text)
    sandbox=Module(:TeacherNotebookAudit)
    Base.include(sandbox,joinpath(stage,"notebook.jl"))
    r=Base.invokelatest(getfield,sandbox,:bao_cao)
    @assert r.chon == [1,2] && r.loi_ich_toi_uu == 14 && r.bat_bien
    @assert r.truy_vet[2].queue == [2] && r.truy_vet[2].spent == 3
    @assert r.truy_vet[3].queue == [1,2] && r.truy_vet[3].spent == 0
    @assert r.truy_vet[4].spent == 8 && r.truy_vet[4].earned == 14
end
println("DAT: notebook mac dinh va hoat dong cung loi Julia, 4 trang thai truyen du lieu.")
