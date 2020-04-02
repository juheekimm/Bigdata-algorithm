## KNN 알고리즘 (K-Nearest Neighbor)

- 이론상으론 새로운 데이터를 입력 받았을 때 가장 가까이 있는것이 무엇인가를 중심으로 그 새로운 데이터의 종류를 정해주는 알고리즘.

- ![image](https://user-images.githubusercontent.com/38865267/78104171-9b86b800-7429-11ea-81f3-4058e5bca12d.png)

- 하지만 이런 경우 ?를 동그라미로 분류하는게 옳은가를 생각해보아야한다.

- ![image](https://user-images.githubusercontent.com/38865267/78104225-c53fdf00-7429-11ea-8f97-343b8fa14d5e.png)

- 그렇기 때문에 좀 더 넓은 시야로 보며 주변에 몇개의 것을 더보게 된다. KNN에서의 K는 주변의 개수를 의미. 

- K번째로 가까운 데이터를 보고 가장 많은 데이터 분류로 들어가게 됨.

- https://firework-ham.tistory.com/27