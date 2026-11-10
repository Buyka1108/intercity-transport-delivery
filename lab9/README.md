\# Лаборатори 9 — Minikube орчинд Deployment, Service үүсгэх



\*\*Хичээл:\*\* CS316 — Программ хангамж хөгжүүлэлтийн процесс



\*\*Төсөл:\*\* Intercity — Хот хоорондын тээвэр ба хүргэлт



\## 1. Багийн бүрэлдэхүүн



| Гишүүн | Оюутны код |

|---|---|

| Ж.Булган | B232270062 |

| Ж.Буянхишиг | B232270114 |

| Э.Бүрэнбаяр | B242270084 |



\## 2. Зорилго



Лаборатори 8-д бүтээсэн Intercity жишээ аппыг Minikube-ийн Kubernetes орчинд гурван хуулбараар ажиллуулж, Service-ээр хандах боломж бүрдүүлэх, нэг Pod устах үед автоматаар нөхөн үүсэх ажиллагааг шалгах.



\## 3. Ашигласан орчин



| Хэрэгсэл | Хувилбар / тохиргоо |

|---|---|

| Docker | 29.5.3 |

| Minikube | v1.39.0 |

| Kubernetes | v1.34.1 |

| kubectl | v1.34.1 |

| Driver | Docker |

| Cluster нөөц | 2 CPU, 3072 MB санах ой |

| Аппын image | intercity-lab9:1.0 |



\## 4. Cluster үүсгэсэн нь



```bat

minikube start --driver=docker --cpus=2 --memory=3072 --kubernetes-version=v1.34.1

minikube status

kubectl --context=minikube wait --for=condition=Ready node/minikube --timeout=180s

kubectl --context=minikube get nodes

```



Эхлэх үед node түр хугацаанд NotReady байсан. Бэлэн болохыг хүлээсний дараа Ready төлөвт шилжсэн.



\## 5. Image бэлтгэсэн нь



Төслийн үндсэн хавтаснаас дараах командуудыг ажиллуулсан:



```bat

docker build -t intercity-lab9:1.0 ./lab8

minikube image load intercity-lab9:1.0

minikube image ls | findstr intercity-lab9

```



Minikube-ийн image жагсаалтад `docker.io/library/intercity-lab9:1.0` гарсан.



\## 6. Deployment ба Service



```bat

kubectl --context=minikube apply -f lab9/deployment.yaml

kubectl --context=minikube apply -f lab9/service.yaml

kubectl --context=minikube rollout status deployment/intercity-app --timeout=180s

```



| Тохиргоо | Утга / зориулалт |

|---|---|

| Deployment | intercity-app |

| replicas | 3 — аппын гурван Pod |

| imagePullPolicy | Never — урьдчилан оруулсан image ашиглана |

| Аппын порт | 3000 |

| Readiness probe | /health — хүсэлт хүлээн авахад бэлэн эсэх |

| Liveness probe | /health — апп хариу өгч байгаа эсэх |

| Service | intercity-service |

| Service төрөл | NodePort |

| Service port → targetPort | 80 → 3000 |

| NodePort | 30080 |



Deployment амжилттай rollout хийж, гурван Pod бүгд `1/1 Running` болсон.



Service нь `app: intercity-app` шошготой, бэлэн Pod-ууд руу хүсэлтийг дамжуулна. `EXTERNAL-IP: <none>` харагдсан нь энэ NodePort Service-ийн хувьд алдаа биш.



\## 7. Апп руу хандсан нь



```bat

minikube service intercity-service

```



Minikube-ийн гаргасан локал холбоосоор вебийг нээсэн. Зураг авах үеийн хаяг `http://127.0.0.1:64358` байсан. Дараагийн ажиллуулалтад энэ порт өөр байж болно.



Windows дээр Docker driver ашиглаж байгаа тул уг командын цонхыг нээлттэй байлгаж хандсан.



!\[Minikube дээр ажиллаж буй Intercity апп](evidence/app-running.png)



Энэ лабораторид Redis байрлуулаагүй тул тоолуур `(memory)` горимоор ажилласан. Pod бүр тусдаа тоолууртай бөгөөд Pod солигдоход тухайн Pod-ийн санах ойн өгөгдөл хадгалагдахгүй. Аяллууд нь жишээ өгөгдөл юм.



\## 8. Автоматаар нөхөн үүсэх туршилт



Эхний гурван Pod:



\- intercity-app-6d69d9f8f5-b45rp

\- intercity-app-6d69d9f8f5-fmlq8

\- intercity-app-6d69d9f8f5-rwqsw



Нэг Pod-ийг зориуд устгасан:



```bat

kubectl --context=minikube delete pod intercity-app-6d69d9f8f5-b45rp

kubectl --context=minikube get pods -l app=intercity-app -w

```



Үр дүн:



| Үзүүлэлт | Ажигласан үр дүн |

|---|---|

| Устгасан Pod | intercity-app-6d69d9f8f5-b45rp |

| Шинээр үүссэн Pod | intercity-app-6d69d9f8f5-jxfjt |

| Бусад хоёр Pod | Ажиллаж хэвээр үлдсэн |

| Эцсийн төлөв | Гурван Pod бүгд 1/1 Running |



!\[Pod автоматаар нөхөн үүссэн үр дүн](evidence/self-healing.png)



Deployment-ийн удирддаг ReplicaSet нь хүссэн гурван Pod-ийн тоог хадгалахын тулд шинэ Pod үүсгэсэн. Устсан Pod өөрөө буцаж ирээгүй, шинэ нэртэй Pod үүссэн.



Энэ туршилт нь Pod устгахад автоматаар нөхөгдөх ажиллагааг баталсан. Апп гацах үеийн liveness probe-ийн үйлчлэлийг тусад нь туршаагүй.



\## 9. Нотлох материал



| Файл | Агуулга |

|---|---|

| deployment.yaml | Гурван хуулбартай Deployment |

| service.yaml | NodePort Service |

| evidence/app-running.png | Kubernetes орчинд ажиллаж буй веб |

| evidence/self-healing.png | Шинэ Pod нөхөн үүссэн үр дүн |

| evidence/pods-before.txt | Устгахаас өмнөх Pod-ууд |

| evidence/pods-after.txt | Нөхөн үүссэний дараах Pod-ууд |

| evidence/deployment-status.txt | Deployment-ийн төлөв |

| evidence/service-status.txt | Service-ийн төлөв |



\## 10. Дүгнэлт



Intercity жишээ аппыг Minikube орчинд гурван Pod-оор ажиллуулж, Service ашиглан браузераас хандав. Нэг Pod-ийг устгахад шинэ Pod автоматаар үүсэж, хүссэн гурван хуулбарын тоо сэргэсэн. Ингэснээр Kubernetes нь тохируулсан төлөвийг хадгалахын тулд Pod-уудыг автоматаар удирддагийг бодит туршилтаар ажиглав.

