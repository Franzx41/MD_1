import pandas as pd
from distancia import jaccard_sim, simpson_corr, hamming_dist

def __split_data(poderes, features, hero_name):
    features.append('hero_names')
    poderes_features = poderes[features]
    hero = poderes_features.loc[poderes_features['hero_names'] == hero_name]

    if hero.shape[0] != 0:
        hero_index = hero.index
        hero_names = poderes_features.drop(hero_index)['hero_names']
        poderes_features = poderes_features.drop('hero_names', axis=1)
        hero_features = poderes_features.iloc[hero_index[0]]
        poder_features = poderes_features.drop(hero_index).reset_index(drop=True)  
    else:
        raise ValueError("heroi não existe no dataset")
        
    return hero_features, poder_features, hero_names

def __similarity_method(metodo):
    if metodo == 'jaccard':
        sim = jaccard_sim
        rank = 'similaridade'
    elif metodo == 'simpson':
        sim = simpson_corr
        rank = 'similaridade'
    elif metodo == 'hamming':
        sim = hamming_dist
        rank = 'distancia'
    else:
        raise ValueError("Metodo não definido")
    return sim, rank

def __sorting(hero_names, similaridades, rank):
    result = pd.DataFrame({"hero_names":hero_names, "similaridade": similaridades})
    if rank == 'similaridade':
        result.sort_values(by=['similaridade'], ascending=False, inplace=True)
    else:
        result.sort_values(by=['similaridade'], ascending=True, inplace=True)
        
    return result

def ranking(poderes, features, hero_name, metodo='jaccard'):
           
    hero_features, poder_features, hero_names = __split_data(poderes, features, hero_name)

    sim, rank = __similarity_method(metodo)


    linhas = poder_features.shape[0]
    similaridades = []
    for i in range(linhas):
        similaridades.append(sim(hero_features, poder_features.iloc[i]))

    result = __sorting(hero_names, similaridades, rank)
        
    return result