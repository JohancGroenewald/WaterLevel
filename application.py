"""Water Level ApplicationUpdate history--------------20190825.2121: Created"""from config import CONFIGimport runrun_loop = run.RunLoop(CONFIG, verbose=1)try:    run_loop.run()except:    run_loop.close()