# Hidden Technical Debt in Machine Learning Systems <br>
* author : 
* society: Google.inc 
* date : 
* link : [[pdf]](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems.pdf)






### Abstract 

머신러닝은 복잡한 예측 시스템을 위한 강력한 도구를 빠르게 제공한다. 본 논문은 이런 빠른 승리들이 
무상으로 제공된다고 생각하는 것은 위험한 생각이라고 주장한다. Software Engineering의 technical debt 프레임워크를 활용하여,
현실속의 머신러닝 시스템에서 계속되는 엄청난 유지보수 비용을 발생시키는 것이 흔한 일임을 알 수 있다. 여러가지 ML-specific 
리스크 요소들을 탐색하여 시스템 디자인에 고려하고자한다. 이러한 요소들에는 1) 경계침식 (boundary erosion) 2) entanglement 
3) hidden feedback loops 4) undeclared consumers 5) data dependencies 6)configuration issues 7) changes in the external world
8) 다양한 시스템 레벨의 anti-patterns가 있다.

Review 

##

### 복잡한 모델은 경계를 침식 시킨다. complex models erode boundaries
- Entanglement
- Correction Cascades
- Undeclared Consumers
- 

### 데이터 의존성은 코드의 존성보다 비싸다. 
- unstable data dependencies
- underutilized data dependencies
  - legacy features
  - bundled features
  - epsilon features
  - correlated features
  - static analysis of data dependencies
  
### 피드백 루프 
- direct feedback loops
- hidden feedback loops

### ML 시스템의 anti-patterns-system anti-patterns
- glue code
- pipeline jungles
- dead experimental codepaths
- abstraction debt
- common smells
  - plain-old-data type smell 
  - multiple-language smell
  - prototype smell
  
### 구성 부채

* 
* 
* 
* 
* 
* 

### 외부 변화 대응
- fixed thresolds in dynamic systems
- monitoring and testing
  - prediction bias (편향 예측) 
  - action limits
  - up-stream producers
  
### 다른 ML관련 부채
- data 테스팅 부채
- 재현성 부채 
- 프로세스 관리 부채
- 문화적 부채 
 
### Conclusions : 부채 측정 및 청산
* 새로운 알고리즘적 접근이 얼마나 쉽게 full-scale test를 할 수 있는가? 
* 모든 data의존성의 transitive closure(이행적 폐쇄)가 무엇인가?
* 새로운 변화의 영향이 얼마나 정확하게 측정 될 수 있는가?
* 한 모델이나 시그널을 발전시키는 것이 다른 것들을 퇴화시키는가?
* 얼마나 빠르게 팀의 새로운 멤버가 팀 작업속도에 따라갈 수 있는가? 








