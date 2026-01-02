
import loopy as lp

def run()->None:
    '''Just prints out the final result. '''
    final_list = lp.query_loop()
    if final_list == False:
        return None
    else:
        for i in final_list[0:2]:
            print(*i)
        print(final_list[-1])
        for i in final_list[2:-1]:
            if(type(i) == str):
                print(i)
            else:
                print(*i)

if __name__ == '__main__':
    run()