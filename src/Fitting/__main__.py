if __name__ == '__main__':
    from fitting import main as main0
    main0()
    from .fit_res import update as res_update
    from .fit_sum import update as sum_update
    res_update()
    sum_update()
