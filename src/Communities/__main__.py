if __name__ == '__main__':
    from .build import main as main0
    main0()
    print('build done')
    from .assign_paper import main as main1p
    main1p()
    print('assign_paper done')
    from .assign_us_patent import main as main1us
    main1us(use_cpc=True)
    print('assign_us_patent done')
    from .assign_cn_patent import main as main1cn
    main1cn(use_cpc=True)
    print('assign_cn_patent done')
    from .assign_ep_patent import main as main1ep
    main1ep(use_cpc=True)
    print('assign_ep_patent done')
    from .pmid2cmnt import main as main2
    main2()
    print('pmid2cmnt done')
    from .pmid2year import main as main3
    main3()
    print('pmid2year done')
    from .sort_by_cmnt import main as main4
    main4()
    print('sort_by_cmnt done')
    from .generate_lohl import main as main7
    main7()
    print('generate_lohl done')
