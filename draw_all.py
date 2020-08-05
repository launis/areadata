def draw_features(X, y, title):
    """
    draw bar features

    args:
        X : X data
        y : y labels
        title : bar title
  
    """
    import numpy as np
    import matplotlib.pyplot as plt
    
    #draw list of features 
    width = 0.4 # the width of the bars 
    ind = np.arange(len(X)) # the x locations for the groups
    plt.barh(ind, X, width, color='green')
    plt.yticks(ind, y)
    plt.title(title)
    plt.xlabel('Relative importance')
    plt.ylabel('Feature') 
    plt.plot(figsize=(20, 20))


def draw_true_vs_predicted(X, y, model, title, binarize=False):
    """
    draw true vs predicted histogram

    args:
        X : X data
        y : y labels
        model: model to be predicted
        title: histogram title
        binarize : in case binarizing is needed
    """
    
    import matplotlib.pyplot as plt
    import numpy as np
    #this point with a histogram both predicted and true
    y_pred =  model.predict(X)
    if binarize:
        y_pred = np.where(model.predict(X)<0.5, 0,1)
    legend = ['True ' + title, 'Predicted ' + title]
    plt.hist([y, y_pred], color=['orange', 'green'])
    plt.ylabel("Frequency")

    plt.legend(legend)
    plt.title('True vs- predicted ' + title)
    plt.plot(figsize=(20, 20))