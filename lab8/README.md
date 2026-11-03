# Лаборатори 8 — Dockerfile бичих Image бүтээх ажиллуулах

**Хичээл:** CS316 — Программ хангамж хөгжүүлэлтийн процесс  
**Оюутан:** Ж.Булган · **Код:** B232270062

## Юу бэлэн байгаа вэ

Node.js-ийн үндсэн http модулиар хийсэн Intercity жишээ апп, Dockerfile, docker-compose.yml, cache шалгах скрипт бэлэн. Аяллын жагсаалт нь жишээ өгөгдөл, бодит захиалга үүсгэхгүй. Compose нь app + Redis гэсэн хоёр контейнерийг хамтад нь ажиллуулна. Redis нь энэ лабын тоолуурын өгөгдлийн сан бөгөөд төслийн эцсийн PostgreSQL сонголтыг өөрчилж байгаа хэрэг биш.

Энэ апп npm dependency-гүй. npm ci нь package-lock.json-ийг ашиглан суулгах алхмыг ажиллуулна; татах нэмэлт package байхгүй. Dockerfile-д dependency файлуудыг эхлээд хуулж, кодыг дараа нь хуулсан тул cache-ийн зарчим хэвээр үйлчилнэ. Уналтын хугацааг зохиомлоор удаашруулаагүй.

## 1 Файлаа зөв байрлуулах

ZIP-ийг задалж `lab8` хавтсыг `C:\Users\zolbi\intercity-transport-delivery` дотор хуулна.

Ингээд `C:\Users\zolbi\intercity-transport-delivery\lab8\Dockerfile` байна.
`lab8\lab8\Dockerfile` гэсэн давхар хавтас үүсгэхгүй.

## 2 Docker Desktop нээх

Docker Desktop-ийг нээгээд Engine ажиллаж дуустал хүлээнэ. Linux containers ашиглана.
CMD дээр команд бүрийг тус тусад нь ажиллуулна:

```bat
cd /d C:\Users\zolbi\intercity-transport-delivery\lab8
docker --version
docker compose version
docker info
```

`docker --version` зөвхөн CLI байгааг хэлнэ. `docker info` дотор Server хэсэг алдаагүй байх нь Engine холбогдсоныг шалгана.
Node.js-ийг компьютер дээр тусад нь суулгах шаардлагагүй, image дотор байна.

## 3 Эхний image бүтээх

```bat
docker build --progress=plain -t intercity-lab8:1.0 . > evidence\build-first.txt 2>&1
type evidence\build-first.txt
docker image ls intercity-lab8
```

Алдаа гарсан бол дараагийн алхам руу орохгүй. `type` командаар эхний build-ийн бодит гаралтыг шалгана.
Командын сүүлийн цэг нь одоогийн lab8 хавтсыг build context болгож байна.

## 4 Контейнер ажиллуулах

```bat
docker run -d --name intercity-lab8-app -p 127.0.0.1:3000:3000 intercity-lab8:1.0
docker ps
docker logs intercity-lab8-app
```

Browser дээр http://localhost:3000 нээнэ. Нэр, оюутны код, v1.0, 3 аялал харагдана.
http://localhost:3000/health дээр status нь ok байна.
Тоолуурын ард `(memory)` харагдана. Энэ нь дан контейнерийн RAM тоолуур; дахин үүсгэхэд тэглэгдэнэ.

## 5 Кодын жижиг өөрчлөлт ба layer caching

Эхний build хийгдсэн байхад дараах командыг CMD дээр ажиллуулна:

```bat
powershell -NoProfile -ExecutionPolicy Bypass -File .\cache-demo.ps1
```

Энэ скрипт зөвхөн `public\index.html` доторх v1.0-ийг v1.1 болгоод дахин build хийнэ.
Тухайн скриптийн нэг процесс дотор execution policy-г тохируулж байгаа бөгөөд компьютерийн байнгын тохиргоог өөрчлөхгүй.

Build output дээр:
- `COPY package.json package-lock.json ./` — CACHED байхыг шалгана.
- `RUN npm ci ...` — CACHED байхыг шалгана.
- `COPY ... server.js ./` — CACHED байхыг шалгана.
- `COPY ... public ./public` — өөрчлөгдсөн тул дахин ажиллана.

Үлдсэн алхмуудын дараалсан invalidation-аас гадна BuildKit нь metadata алхмуудыг оновчилж болох тул зөвхөн мөр бүрийн хугацаагаар дүгнэхгүй. Энэ туршилтын гол нотолгоо нь npm ci cached хэвээр, өөрчилсөн public COPY дахин ажилласан гаралт.

Терминалын энэ хэсгийг **Win + Shift + S** ашиглан зураг авч `evidence\build-cache.png` нэрээр хадгална.
Гаралт мөн `evidence\build-cache.txt` дотор хадгалагдана.

Шинэ image-ээр контейнерээ дахин үүсгэнэ:

```bat
docker stop intercity-lab8-app
docker rm intercity-lab8-app
docker run -d --name intercity-lab8-app -p 127.0.0.1:3000:3000 intercity-lab8:1.1
```

Browser дээр Ctrl + F5 дарна. **v1.1** болсон байна.
URL, апп, нэр/код харагдах screenshot авч **evidence\app-running.png** нэрээр хадгална.
Image-ийг дахин build хийсэн төдийд өмнөх контейнер шинэчлэгдэхгүй тул дээр дахин үүсгэж байна.

## 6 Docker Compose — хоёр сервис хамт ажиллуулах

Эхлээд 3000 порт ашиглаж байгаа дан контейнерийг зогсооно:

```bat
docker stop intercity-lab8-app
docker rm intercity-lab8-app
docker compose up --build -d
docker compose ps
docker compose logs --tail=30 app redis
```

app, redis гэсэн хоёр сервис ажиллана. http://localhost:3000 нээгээд тоолуурын ард **(redis)** байгааг шалгана. Refresh бүрд тоолуур нэмэгдэнэ.
App контейнер нь Redis рүү `localhost` биш Compose-ийн `redis` сервисийн нэрээр холбогдоно.
Redis-ийн порт компьютер рүү нийтлэгдээгүй, зөвхөн Compose-ийн дотоод сүлжээнд ашиглагдана.

Хадгалалтыг шалгах:

```bat
docker compose down
docker compose up -d
```

Дахин хуудас нээхэд тоолуур өмнөхөөс үргэлжилнэ. AOF + named volume хадгалдаг.
Энэ шалгалтад `down -v` ашиглахгүй, учир нь volume-ийн өгөгдлийг устгана.
Compose-ийн `ps` ба browser-ийн redis тоолууртай нэмэлт screenshot авч болно.

## 7 Багшид өгөх зүйл

Лабын зураг дээрх үндсэн deliverable:
1. Dockerfile.
2. app-running.png — ажиллаж буй апп.
3. build-cache.png — кодын жижиг өөрчлөлтийн дараах build output.

Лабын бүх алхмыг хамруулахын тулд docker-compose.yml, аппын эх код, build-first.txt, build-cache.txt-ийг хамт өгнө.
Нэмэлтээр `compose.png` хадгалж болно. Бодит build output гарахаас өмнө хийсэн гэж тайлагнахгүй.

## 8 Dockerfile мөрүүдийн тайлбар

| Мөр | Үүрэг |
|---|---|
| FROM node:22-alpine | Node.js агуулсан суурь image сонгоно. |
| WORKDIR /app | Контейнер дотор ажиллах хавтсыг тогтооно. |
| COPY package.json package-lock.json ./ | Dependency мэдээллийг эхлээд хуулна. |
| RUN npm ci ... | Lock файлд тулгуурласан суулгах алхам; энэ апп нэмэлт dependency-гүй. |
| COPY server.js; COPY public | Сервер болон веб хуудасны кодыг хуулна. |
| ENV | Аппын тохиргоог өгнө. |
| USER node | Аппыг root бус хэрэглэгчээр ажиллуулна. |
| EXPOSE 3000 | Аппын контейнер дотор сонсох портыг баримтжуулна. Портыг нийтлэхгүй. |
| CMD | Контейнер эхлэхэд node server.js ажиллуулна. |

`docker run -p` болон Compose-ийн ports нь компьютерийн портыг контейнертэй холбоно.
Апп `0.0.0.0` дээр сонсдог тул контейнерийн гаднаас нийтэлсэн портоор хүрэх боломжтой.
`.dockerignore` нь Git, лог, нотолгоо, node_modules-ийг image рүү оруулахгүй.

## 9 Түгээмэл алдаа

- **Docker daemon/engine холбогдохгүй:** Docker Desktop нээгээд `docker info` дахин ажиллуулна.
- **Port 3000 already allocated:** өөр апп/хуучин контейнер 3000 ашиглаж байна. Түүнийг зогсоох эсвэл `-p 127.0.0.1:3008:3000` ашиглаад localhost:3008 нээнэ. Compose-д зүүн талын 3000-ийг мөн 3008 болгоно.
- **Container name already in use:** `docker ps -a`-гаар шалгаад зөвхөн энэ лабын хуучин контейнерийг stop, rm хийнэ.
- **failed to read dockerfile:** `dir` гэж шалгана. Dockerfile одоогийн хавтсанд байх ёстой; Dockerfile.txt байж болохгүй.
- **Image татагдахгүй:** интернэт болон Docker Desktop-ийн сүлжээний тохиргоог шалгана.
- **Redis unavailable:** `docker compose ps`, `docker compose logs redis` шалгана. `/health` нь app-ийн liveness, харин `/api/visits` нь Redis ажиллагааг давхар шалгана.

## 10 GitHub руу оруулах

Өмнөх өөрчлөлтүүдээ шалгаж байж repository-ийн үндсэн хавтсанд шинэ branch нээнэ:

```bat
cd /d C:\Users\zolbi\intercity-transport-delivery
git status
git switch -c feature/lab8-docker
git add lab8
git diff --cached --check
git commit -m "Add Lab 8 Docker app Compose and cache evidence"
git push -u origin feature/lab8-docker
```

Дараа нь GitHub дээр PR нээж, Files changed болон боломжтой CI checks-ийг шалгана.
Энэ нь өмнөх Лаб6/7-ийн эх кодыг өөрчлөхгүй.

## Эх сурвалж

- Өгсөн Лаборатори 8-ын зааврын зураг.
- https://docs.docker.com/build/cache/optimize/
- https://docs.docker.com/get-started/docker-concepts/building-images/using-the-build-cache/

## Бэлтгэлийн шалгалтын хязгаар

Аппыг Node.js дээр, Redis protocol-ийг түр mock сервертэй шалгасан. Энэ багцыг бэлтгэсэн орчинд Docker CLI/Engine байхгүй тул image build, Docker Compose ажиллуулалтын үр дүн болон screenshot-уудыг хэрэглэгчийн компьютер дээр баталгаажуулна. Mock шалгалт нь бодит Redis контейнертэй шалгалтыг орлохгүй.
