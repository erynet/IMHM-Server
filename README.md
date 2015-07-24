# GET /users/
유저들 가져오기

#### Header
+ 없음

#### Parameters
+ 없음 

#### Response
+ `200` ... 성공

	```json
	{
	  "users": [
		{
		  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
		  "auth": false, 
		  "car_num": "4111", 
		  "created_at": 1432006370.0, 
		  "detail_address": "\u314e\u314e\u314e", 
		  "id": 1, 
		  "main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
		  "name": "\uae40\uae40\uae40", 
		  "office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
		  "updated_at": 1432019572.0, 
		  "username": "kim0123"
		}
	  ]
	}
	```

#### Keys Description
+ `users` ... 유저들을 담은 list
	+ `user` ... 유저 객체
		+ `id` ... db 인덱스
		+ `name` ... 이름
		+ `username` ... 아이디
		+ `address` ... 통합 주소
		+ `main_address` ... 첫번째 주소
		+ `detail_address` ... 상세 주소
		+ `office` ... 소재지
		+ `auth` ... 승인 여부 
		+ `car_num` ... 차량 번호
		+ `created_at` ... 생성 시간 타임스탬프
		+ `updated_at` ... 업데이트 시간 타임스탬프

# GET /user/\<username>/
특정 유저 가져오기

#### Header
+ 없음

#### Parameters
+ 없음 

#### Response
+ `200` ... 성공

	```json
	{
	  "user":
		{
		  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
		  "auth": false, 
		  "car_num": "4111", 
		  "created_at": 1432006370.0, 
		  "detail_address": "\u314e\u314e\u314e", 
		  "id": 1, 
		  "main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
		  "name": "\uae40\uae40\uae40", 
		  "office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
		  "updated_at": 1432019572.0, 
		  "username": "kim0123"
		}
	}
	```

#### Keys Description
+ `user` ... 유저 객체
	+ `id` ... db 인덱스
	+ `name` ... 이름
	+ `username` ... 아이디
	+ `address` ... 통합 주소
	+ `main_address` ... 첫번째 주소
	+ `detail_address` ... 상세 주소
	+ `office` ... 소재지
	+ `auth` ... 승인 여부 
	+ `car_num` ... 차량 번호
	+ `created_at` ... 생성 시간 타임스탬프
	+ `updated_at` ... 업데이트 시간 타임스탬프
	
# DELETE /user/\<username>/
특정 유저 삭제

#### Header
+ `Content-Type` : `application/json`

#### Parameters
+ `password` ... 패스워드

#### Response
+ `200` ... 성공

	```json
	{
	  "user":
		{
		  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
		  "auth": false, 
		  "car_num": "4111", 
		  "created_at": 1432006370.0, 
		  "detail_address": "\u314e\u314e\u314e", 
		  "id": 1, 
		  "main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
		  "name": "\uae40\uae40\uae40", 
		  "office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
		  "updated_at": 1432019572.0, 
		  "username": "kim0123"
		}
	}
	```

#### Keys Description
+ `user` ... 유저 객체
	+ `id` ... db 인덱스
	+ `name` ... 이름
	+ `username` ... 아이디
	+ `address` ... 통합 주소
	+ `main_address` ... 첫번째 주소
	+ `detail_address` ... 상세 주소
	+ `office` ... 소재지
	+ `auth` ... 승인 여부 
	+ `car_num` ... 차량 번호
	+ `created_at` ... 생성 시간 타임스탬프
	+ `updated_at` ... 업데이트 시간 타임스탬프


# GET /user/\<username>/exist/
닉네임 중복체크

#### Header
+ 없음

#### Parameters
+ 없음 

#### Response
+ `200` ... 성공

	```json
{
  "exist": false
}
	```

#### Keys Description
+ `exist` : 존재 여부


# POST /user/
유저 생성하기

#### Header
+ `Content-Type` : `application/json`

#### Parameters
+ `name` ... 이름 
+ `username` ... 아이디 
+ `password` ... 패스워드
+ `car_num` ... 차량 번호
+ `main_address` ... 첫번째 주소
+ `detail_address` ... 상세 주소
+ `office` ... 소재지

#### Response
+ `200` ... 성공

	```json
	{"user": {"address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9",
			   "auth": False,
			   "car_num": "4111",
			   "created_at": 1432006370.0,
			   "main_address": "\u314e\u314e\u314e",
			   "detail_address": "\u314e\u314e\u314e",
			   "id": 1,
			   "name": "\uae40\uae40\uae40",
			   "office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f",
			   "updated_at": 1432006370.0,
			   "username": "kim0123"}}
	```

+ `409` ... 존재하는 아이디


#### Keys Description
+ `user` ... 유저 객체
	+ `id` ... db 인덱스
	+ `name` ... 이름
	+ `username` ... 아이디
	+ `address` ... 통합 주소
	+ `main_address` ... 첫번째 주소
	+ `detail_address` ... 상세 주소
	+ `office` ... 소재지
	+ `auth` ... 승인 여부 
	+ `car_num` ... 차량 번호
	+ `created_at` ... 생성 시간 타임스탬프
	+ `updated_at` ... 업데이트 시간 타임스탬프

# POST /user/\<username>/login
로그인하기

#### Header
+ `Content-Type` : `application/json`

#### Response
+ `200` ... 성공

	```json
	{
	"user": {"address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9",
			   "auth": False,
			   "car_num": "4111",
			   "created_at": 1432006370.0,
			   "main_address": "\u314e\u314e\u314e",
			   "detail_address": "\u314e\u314e\u314e",
			   "id": 1,
			   "name": "\uae40\uae40\uae40",
			   "office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f",
			   "updated_at": 1432006370.0,
			   "username": "kim0123"}
   }
	```

+ `409` ... 존재하는 아이디


#### Keys Description
+ `user` ... 유저 객체
	+ `id` ... db 인덱스
	+ `name` ... 이름
	+ `username` ... 아이디
	+ `address` ... 통합 주소
	+ `main_address` ... 첫번째 주소
	+ `detail_address` ... 상세 주소
	+ `office` ... 소재지
	+ `auth` ... 승인 여부 
	+ `car_num` ... 차량 번호
	+ `created_at` ... 생성 시간 타임스탬프
	+ `updated_at` ... 업데이트 시간 타임스탬프


# GET /orders/
오더들 가져오기

#### Header
+ 없음

#### Parameters
+ 없음 

#### Response
+ `200` ... 성공

	```json
	{
	  "orders": [
		   {
		  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c13\ub3d9\u314e\u314e\u314e", 
		  "created_at": 1432007881.0, 
		  "date": "2014-01-23", 
		  "detail_address": "\u314e\u314e\u314e", 
		  "floor": 3, 
		  "id": 1, 
		  "orderer": {
			"address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
			"auth": false, 
			"car_num": "4111", 
			"created_at": 1432006370.0, 
			"detail_address": "\u314e\u314e\u314e", 
			"id": 1, 
			"main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
			"name": "\uae40\uae40\uae40", 
			"office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
			"updated_at": 1432019572.0, 
			"username": "kim0123"
		  }, 
		  "orderer_id": 1, 
		  "phone": "010-0120-2020", 
		  "price": "5000", 
		  "status": 0, 
		  "ton": 3.0, 
		  "updated_at": 1432020467.0
		}
	  ]
	}
	```

#### Keys Description
+ `orders` ... 오더들을 담은 list
	+ `order` ... 오더 객체 
		+ `id` ... db 인덱스 
		+ `date` ... 이사 날짜
		+ `address` ... 통합 주소
		+ `main_address` ... 첫번째 주소
		+ `detail_address` ... 상세 주소
		+ `floor` ... 층
		+ `ton` ... 톤
		+ `phone` ... 전화번호
		+ `price` ... 비용
		+ `status` ... 오더 상태 
			+ `0` ... 배차 대기
			+ `1` ... 작업중
			+ `2` ... 배차 완료
		+ `orderer` ... 배차 요청자 객체
		+ `orderer_id` ... 배차 요청자 db 인덱스
		+ `orderee` ... 배차 작업자 객체 (배차 대기 상태에는 존재하지 않음)
		+ `orderee_id` ... 배차 작업자 db 인덱스

# GET /order/\<idx>/
특정 오더 가져오기

#### Header
+ 없음

#### Parameters
+ 없음 

#### Response
+ `200` ... 성공

	```json
	{"order":	{
	  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c13\ub3d9\u314e\u314e\u314e", 
	  "created_at": 1432007881.0, 
	  "date": "2014-01-23", 
	  "detail_address": "\u314e\u314e\u314e", 
	  "floor": 3, 
	  "id": 1, 
	  "orderer": {
		"address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
		"auth": false, 
		"car_num": "4111", 
		"created_at": 1432006370.0, 
		"detail_address": "\u314e\u314e\u314e", 
		"id": 1, 
		"main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
		"name": "\uae40\uae40\uae40", 
		"office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
		"updated_at": 1432019572.0, 
		"username": "kim0123"
	  }, 
	  "orderer_id": 1, 
	  "phone": "010-0120-2020", 
	  "price": "5000", 
	  "status": 0, 
	  "ton": 3.0, 
	  "updated_at": 1432020467.0
	}}
	```
+ `404` ... 없는 오더


#### Keys Description
+ `order` ... 오더 객체
	+ `id` ... db 인덱스 
	+ `date` ... 이사 날짜
	+ `address` ... 통합 주소
	+ `main_address` ... 첫번째 주소
	+ `detail_address` ... 상세 주소
	+ `floor` ... 층
	+ `ton` ... 톤
	+ `phone` ... 전화번호
	+ `price` ... 비용
	+ `status` ... 오더 상태 
		+ `0` ... 배차 대기
		+ `1` ... 작업중
		+ `2` ... 배차 완료
	+ `orderer` ... 배차 요청자 객체
	+ `orderer_id` ... 배차 요청자 db 인덱스
	+ `orderee` ... 배차 작업자 객체 (배차 대기 상태에는 존재하지 않음)
	+ `orderee_id` ... 배차 작업자 db 인덱스

# GET /order/address/\<address>
지역 검색

#### Header
+ 없음

#### Parameters
+ 없음 

#### Response
+ `200` ... 성공

	```json
	{
	  "orders": [
		{
		  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c13\ub3d9\u314e\u314e\u314e", 
		  "created_at": 1432007881.0, 
		  "date": "2014-01-23", 
		  "detail_address": "\u314e\u314e\u314e", 
		  "floor": 3, 
		  "id": 1, 
		  "orderer": {
			"address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
			"auth": false, 
			"car_num": "4111", 
			"created_at": 1432006370.0, 
			"detail_address": "\u314e\u314e\u314e", 
			"id": 1, 
			"main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
			"name": "\uae40\uae40\uae40", 
			"office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
			"updated_at": 1432019572.0, 
			"username": "kim0123"
		  }, 
		  "orderer_id": 1, 
		  "phone": "010-0120-2020", 
		  "price": "5000", 
		  "status": 0, 
		  "ton": 3.0, 
		  "updated_at": 1432020467.0
		}
	  ]
	}
	```


#### Keys Description
+ `orders` ... 오더들을 담은 list
	+ `order` ... 오더 객체 
		+ `id` ... db 인덱스 
		+ `date` ... 이사 날짜
		+ `address` ... 통합 주소
		+ `main_address` ... 첫번째 주소
		+ `detail_address` ... 상세 주소
		+ `floor` ... 층
		+ `ton` ... 톤
		+ `phone` ... 전화번호
		+ `price` ... 비용
		+ `status` ... 오더 상태 
			+ `0` ... 배차 대기
			+ `1` ... 작업중
			+ `2` ... 배차 완료
		+ `orderer` ... 배차 요청자 객체
		+ `orderer_id` ... 배차 요청자 db 인덱스
		+ `orderee` ... 배차 작업자 객체 (배차 대기 상태에는 존재하지 않음)
		+ `orderee_id` ... 배차 작업자 db 인덱스

# GET /order/floor/
층 수 검색

#### Header
+ 없음

#### Parameters
+ `max` ... 최고층
+ `min` ... 최하층

#### Response
+ `200` ... 성공

	```json
	{
	  "orders": [
		{
		  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c13\ub3d9\u314e\u314e\u314e", 
		  "created_at": 1432007881.0, 
		  "date": "2014-01-23", 
		  "detail_address": "\u314e\u314e\u314e", 
		  "floor": 3, 
		  "id": 1, 
		  "orderer": {
			"address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
			"auth": false, 
			"car_num": "4111", 
			"created_at": 1432006370.0, 
			"detail_address": "\u314e\u314e\u314e", 
			"id": 1, 
			"main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
			"name": "\uae40\uae40\uae40", 
			"office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
			"updated_at": 1432019572.0, 
			"username": "kim0123"
		  }, 
		  "orderer_id": 1, 
		  "phone": "010-0120-2020", 
		  "price": "5000", 
		  "status": 0, 
		  "ton": 3.0, 
		  "updated_at": 1432020467.0
		}
	  ]
	}
	```


#### Keys Description
+ `orders` ... 오더들을 담은 list
	+ `order` ... 오더 객체 
		+ `id` ... db 인덱스 
		+ `date` ... 이사 날짜
		+ `address` ... 통합 주소
		+ `main_address` ... 첫번째 주소
		+ `detail_address` ... 상세 주소
		+ `floor` ... 층
		+ `ton` ... 톤
		+ `phone` ... 전화번호
		+ `price` ... 비용
		+ `status` ... 오더 상태 
			+ `0` ... 배차 대기
			+ `1` ... 작업중
			+ `2` ... 배차 완료
		+ `orderer` ... 배차 요청자 객체
		+ `orderer_id` ... 배차 요청자 db 인덱스
		+ `orderee` ... 배차 작업자 객체 (배차 대기 상태에는 존재하지 않음)
		+ `orderee_id` ... 배차 작업자 db 인덱스

# GET /order/price/
비용 검색

#### Header
+ 없음

#### Parameters
+ `max` ... 최대 비용
+ `min` ... 최하 비용

#### Response
+ `200` ... 성공

	```json
	{
	  "orders": [
		{
		  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c13\ub3d9\u314e\u314e\u314e", 
		  "created_at": 1432007881.0, 
		  "date": "2014-01-23", 
		  "detail_address": "\u314e\u314e\u314e", 
		  "floor": 3, 
		  "id": 1, 
		  "orderer": {
			"address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
			"auth": false, 
			"car_num": "4111", 
			"created_at": 1432006370.0, 
			"detail_address": "\u314e\u314e\u314e", 
			"id": 1, 
			"main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
			"name": "\uae40\uae40\uae40", 
			"office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
			"updated_at": 1432019572.0, 
			"username": "kim0123"
		  }, 
		  "orderer_id": 1, 
		  "phone": "010-0120-2020", 
		  "price": "5000", 
		  "status": 0, 
		  "ton": 3.0, 
		  "updated_at": 1432020467.0
		}
	  ]
	}
	```


#### Keys Description
+ `orders` ... 오더들을 담은 list
	+ `order` ... 오더 객체 
		+ `id` ... db 인덱스 
		+ `date` ... 이사 날짜
		+ `address` ... 통합 주소
		+ `main_address` ... 첫번째 주소
		+ `detail_address` ... 상세 주소
		+ `floor` ... 층
		+ `ton` ... 톤
		+ `phone` ... 전화번호
		+ `price` ... 비용
		+ `status` ... 오더 상태 
			+ `0` ... 배차 대기
			+ `1` ... 작업중
			+ `2` ... 배차 완료
		+ `orderer` ... 배차 요청자 객체
		+ `orderer_id` ... 배차 요청자 db 인덱스
		+ `orderee` ... 배차 작업자 객체 (배차 대기 상태에는 존재하지 않음)
		+ `orderee_id` ... 배차 작업자 db 인덱스

# GET /order/unsolved/
미해결 검색

#### Header
+ 없음

#### Parameters
+ 없음

#### Response
+ `200` ... 성공

	```json
	{
	  "orders": [
		{
		  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c13\ub3d9\u314e\u314e\u314e", 
		  "created_at": 1432007881.0, 
		  "date": "2014-01-23", 
		  "detail_address": "\u314e\u314e\u314e", 
		  "floor": 3, 
		  "id": 1, 
		  "orderer": {
			"address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
			"auth": false, 
			"car_num": "4111", 
			"created_at": 1432006370.0, 
			"detail_address": "\u314e\u314e\u314e", 
			"id": 1, 
			"main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
			"name": "\uae40\uae40\uae40", 
			"office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
			"updated_at": 1432019572.0, 
			"username": "kim0123"
		  }, 
		  "orderer_id": 1, 
		  "phone": "010-0120-2020", 
		  "price": "5000", 
		  "status": 0, 
		  "ton": 3.0, 
		  "updated_at": 1432020467.0
		}
	  ]
	}
	```


#### Keys Description
+ `orders` ... 오더들을 담은 list
	+ `order` ... 오더 객체 
		+ `id` ... db 인덱스 
		+ `date` ... 이사 날짜
		+ `address` ... 통합 주소
		+ `main_address` ... 첫번째 주소
		+ `detail_address` ... 상세 주소
		+ `floor` ... 층
		+ `ton` ... 톤
		+ `phone` ... 전화번호
		+ `price` ... 비용
		+ `status` ... 오더 상태 
			+ `0` ... 배차 대기
			+ `1` ... 작업중
			+ `2` ... 배차 완료
		+ `orderer` ... 배차 요청자 객체
		+ `orderer_id` ... 배차 요청자 db 인덱스
		+ `orderee` ... 배차 작업자 객체 (배차 대기 상태에는 존재하지 않음)
		+ `orderee_id` ... 배차 작업자 db 인덱스


# POST /order/
오더 생성하기

#### Header
+ `Content-Type` : `application/json`

#### Parameters
+ `username` ... 아이디 
+ `password` ... 패스워드
+ `date (YYYY-MM-DD)` ... 이사 일정
+ `ton (float)` ... 무게
+ `floor (int)` ... 층
+ `phone` ... 휴대폰 번호
+ `address` ... 통합 주소
+ `main_address` ... 첫번째 주소
+ `detail_address` ... 상세 주소
+ `price (str)` ... 가격 

#### Response
+ `200` ... 성공

	```json
	{
		"order":	{
		  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c13\ub3d9\u314e\u314e\u314e", 
		  "created_at": 1432007881.0, 
		  "date": "2014-01-23", 
		  "detail_address": "\u314e\u314e\u314e", 
		  "floor": 3, 
		  "id": 1, 
		  "orderer": {
			"address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
			"auth": false, 
			"car_num": "4111", 
			"created_at": 1432006370.0, 
			"detail_address": "\u314e\u314e\u314e", 
			"id": 1, 
			"main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
			"name": "\uae40\uae40\uae40", 
			"office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
			"updated_at": 1432019572.0, 
			"username": "kim0123"
		  }, 
		  "orderer_id": 1, 
		  "phone": "010-0120-2020", 
		  "price": "5000", 
		  "status": 0, 
		  "ton": 3.0, 
		  "updated_at": 1432020467.0
		}
	}
	```

+ `400` ... 인자 오류
+ `401` ... 인증 오류 (패스워드 오류)
+ `404` ... 없는 유저
+ `409` ... 존재하는 아이디


#### Keys Description
+ `order` ... 오더 객체
	+ `id` ... db 인덱스 
	+ `date` ... 이사 날짜
	+ `address` ... 통합 주소
	+ `main_address` ... 첫번째 주소
	+ `detail_address` ... 상세 주소
	+ `floor` ... 층
	+ `ton` ... 톤
	+ `phone` ... 전화번호
	+ `price` ... 비용
	+ `status` ... 오더 상태 
		+ `0` ... 배차 대기
		+ `1` ... 작업중
		+ `2` ... 배차 완료
	+ `orderer` ... 배차 요청자 객체
	+ `orderer_id` ... 배차 요청자 db 인덱스
	+ `orderee` ... 배차 작업자 객체 (배차 대기 상태에는 존재하지 않음)
	+ `orderee_id` ... 배차 작업자 db 인덱스
	
# POST /order/\<idx>/
오더 작업 요청하기

#### Header
+ `Content-Type` : `application/json`

#### Parameters
+ `username` ... 아이디 
+ `password` ... 패스워드

#### Response
+ `200` ... 성공

	```json
	{
		"order":	{
		  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c13\ub3d9\u314e\u314e\u314e", 
		  "created_at": 1432007881.0, 
		  "date": "2014-01-23", 
		  "detail_address": "\u314e\u314e\u314e", 
		  "floor": 3, 
		  "id": 1, 
		  "orderer": {
			"address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
			"auth": false, 
			"car_num": "4111", 
			"created_at": 1432006370.0, 
			"detail_address": "\u314e\u314e\u314e", 
			"id": 1, 
			"main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
			"name": "\uae40\uae40\uae40", 
			"office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
			"updated_at": 1432019572.0, 
			"username": "kim0123"
		  }, 
		  "orderer_id": 1, 
		  "phone": "010-0120-2020", 
		  "price": "5000", 
		  "status": 1, 
		  "ton": 3.0, 
		  "updated_at": 1432020467.0
		}
	}
	```

+ `400` ... 인자 오류
+ `401` ... 인증 오류 (패스워드 오류)
+ `404` ... 없는 오더


#### Keys Description
+ `order` ... 오더 객체
	+ `id` ... db 인덱스 
	+ `date` ... 이사 날짜
	+ `address` ... 통합 주소
	+ `main_address` ... 첫번째 주소
	+ `detail_address` ... 상세 주소
	+ `floor` ... 층
	+ `ton` ... 톤
	+ `phone` ... 전화번호
	+ `price` ... 비용
	+ `status` ... 오더 상태 
		+ 0 ... 배차 대기
		+ 1 ... 작업중
		+ 2 ... 배차 완료
	+ `orderer` ... 배차 요청자 객체
	+ `orderer_id` ... 배차 요청자 db 인덱스
	+ `orderee` ... 배차 작업자 객체 (배차 대기 상태에는 존재하지 않음)
	+ `orderee_id` ... 배차 작업자 db 인덱스

# POST /order\/<idx>\/status\/
오더 작업 상태 변경

#### Header
+ `Content-Type` : `application/json`

#### Parameters
+ `username` ... 아이디 
+ `password` ... 패스워드
+ `status` ... 변경할 상태 코드
	+ `0` ... 배차 대기
	+ `1` ... 작업중
	+ `2` ... 배차 완료


#### Response
+ `200` ... 성공

	```json
	{
		"order":	{
		  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c13\ub3d9\u314e\u314e\u314e", 
		  "created_at": 1432007881.0, 
		  "date": "2014-01-23", 
		  "detail_address": "\u314e\u314e\u314e", 
		  "floor": 3, 
		  "id": 1, 
		  "orderer": {
			"address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
			"auth": false, 
			"car_num": "4111", 
			"created_at": 1432006370.0, 
			"detail_address": "\u314e\u314e\u314e", 
			"id": 1, 
			"main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
			"name": "\uae40\uae40\uae40", 
			"office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
			"updated_at": 1432019572.0, 
			"username": "kim0123"
		  }, 
		  "orderer_id": 1, 
		  "phone": "010-0120-2020", 
		  "price": "5000", 
		  "status": 1, 
		  "ton": 3.0, 
		  "updated_at": 1432020467.0
		}
	}
	```

+ `400` ... 인자 오류
+ `401` ... 인증 오류 (패스워드 오류)
+ `403` ... 오더와 관련된 자 (등록자, 배차자) 가 아닌 경우
+ `404` ... 없는 오더
+ `409` ... 변경 불가능한 상태 변경을 요청할 경우 (ex. 등록자가 "작업중"을 "배차 대기"로 변경)


#### Keys Description
+ `order` ... 오더 객체
	+ `id` ... db 인덱스 
	+ `date` ... 이사 날짜
	+ `address` ... 통합 주소
	+ `main_address` ... 첫번째 주소
	+ `detail_address` ... 상세 주소
	+ `floor` ... 층
	+ `ton` ... 톤
	+ `phone` ... 전화번호
	+ `price` ... 비용
	+ `status` ... 오더 상태 
		+ `0` ... 배차 대기
		+ `1` ... 작업중
		+ `2` ... 배차 완료
	+ `orderer` ... 배차 요청자 객체
	+ `orderer_id` ... 배차 요청자 db 인덱스
	+ `orderee` ... 배차 작업자 객체 (배차 대기 상태에는 존재하지 않음)
	+ `orderee_id` ... 배차 작업자 db 인덱스
	

# GET /version/\<os>/
버전 정보 가져오기

#### Header
+ 없음

#### Parameters
+ `os (in uri)`
	+ `가능 인자`
		+ `Android (대소문자 구별)` ... 안드로이드 버전 정보 가져오기 

#### Response
+ `200` ... 성공

	```json
	{
	  "version": "1.0.0"
	}
	```


#### Keys Description
+ `version (str)` ... 버전 정보


# GET /terms/ktclub/
ktclub 소개글

#### Header
+ 없음

#### Parameters
+ 없음

#### Response
+ `200` ... 성공

	```html
	소개글소개글소개글소개글소개글소개글소개글소개글
	```

#### Keys Description
+ 없음

# GET /notifications/
공지사항들 가져오기

#### Header
+ 없음

#### Parameters
+ `filters` ... 가져올 정보들
	+ `기본` ... 인자로 넘기지 않아도 리턴되는 값들
		+ `id` ... db 인덱스
		+ `author`... 글쓴이 객체
		+ `created_at (timestamp)` ... 작성 일자
		+ `updated_at (timestamp)` ... 업데이트 일자
	+ `가능 인자`
		+ `title` ... 공지 제목
		+ `content` ... 공지 내용
	+ `예제`
		+ `/notifications/?filters=title,content`

#### Response
+ `200` ... 성공

	```json
	{
	  "notifications": [
		{
		  "author": {
			"created_at": 1435804200,
			"id": 1,
			"login": "421",
			"name": "홍길동",
			"point": 92342,
			"regular_at": 1435804191,
			"regular_member": true,
			"updated_at": 1435804202,
			"username": "hgd",
			"uuid": "1234567fgsdf"
		  },
		  "content": "수정된-가나다라마$!@$asd12412D@!2",
		  "created_at": 1435805307,
		  "id": 4,
		  "title": "수정된테스트4",
		  "updated_at": 1435844819
		},
		{
		  "author": {
			"created_at": 1435804200,
			"id": 1,
			"login": "421",
			"name": "홍길동",
			"point": 92342,
			"regular_at": 1435804191,
			"regular_member": true,
			"updated_at": 1435804202,
			"username": "hgd",
			"uuid": "1234567fgsdf"
		  },
		  "content": "가나다라마$!@$asd12412D@!2",
		  "created_at": 1435838135,
		  "id": 6,
		  "title": "테스트6",
		  "updated_at": 1435838135
		}
	  ]
	}
	```

#### Keys Description
+ `notifications` ... 공지사항들을 담은 list
	+ `notifiaction` ... 인자로 넘기지 않아도 리턴되는 값들
		+ `id` ... db 인덱스
		+ `author`... 글쓴이 객체
		+ `created_at (timestamp)` ... 작성 일자
		+ `updated_at (timestamp)` ... 업데이트 일자
		+ `title (선택시)` ... 공지 제목
		+ `content (선택시)` ... 공지 내용
		+ `author_id (선택시)` ... 글쓴이 db 인덱스

# GET /notification/read/\<idx>/
특정 공지사항 가져오기

#### Header
+ 없음

#### Parameters
+ 없음

#### Response
+ `200` ... 성공

	```json
	{
	  "notification": {
		"author": {
		  "code": "abc", 
		  "created_at": 1432073134.0, 
		  "id": 1, 
		  "name": "admin", 
		  "updated_at": 1432073134.0, 
		  "username": "admin123"
		}, 
		"author_id": 1, 
		"content": "notinotinotinotinotinotinoti", 
		"created_at": 1432073155.0, 
		"id": 1, 
		"title": "noti1", 
		"updated_at": 1432073155.0
	  }
	}
	```

#### Keys Description
+ `notifications` ... 공지사항들을 담은 list
	+ `notifiaction` ... 인자로 넘기지 않아도 리턴되는 값들
		+ `id` ... db 인덱스
		+ `author`... 글쓴이 객체
		+ `created_at (timestamp)` ... 작성 일자
		+ `updated_at (timestamp)` ... 업데이트 일자
		+ `title (선택시)` ... 공지 제목
		+ `content (선택시)` ... 공지 내용
		+ `author_id (선택시)` ... 글쓴이 db 인덱스

# POST /notification/write/
공지사항들 쓰기

#### Header
+ `Content-Type` : `application/json`

#### Parameters
+ `title` ... 제목 
+ `content` ... 내용 
+ `author_id` ... 작성한 관리자 id

#### Response
+ `400` ... 필요한 파라메터가 제대로 오지 않았음
+ `401` ... 올바르지 않은 author_id 
+ `200` ... 성공 

	```json
	{
	  "notifications": [
		{
		  "author": {
			"code": "abc", 
			"created_at": 1432073134.0, 
			"id": 1, 
			"name": "admin", 
			"updated_at": 1432073134.0, 
			"username": "admin123"
		  }, 
		  "author_id": 1, 
		  "content": "가나다라마$!@$asd12412D@!2", 
		  "created_at": 1432073155.0, 
		  "id": 1, 
		  "title": "noti1", 
		  "updated_at": 1432073155.0
		}
	  ]
	}
	```

#### Keys Description
+ `notifications` ... 공지사항들을 담은 list
	+ `notifiaction` ... 인자로 넘기지 않아도 리턴되는 값들
		+ `id` ... db 인덱스
		+ `author`... 글쓴이 객체
		+ `created_at (timestamp)` ... 작성 일자
		+ `updated_at (timestamp)` ... 업데이트 일자
		+ `title` ... 공지 제목
		+ `content` ... 공지 내용
		+ `author_id` ... 글쓴이 db 인덱스
		
# PUT /notification/update/\<idx>/
공지사항들 갱신하기

#### Header
+ `Content-Type` : `application/json`

#### Parameters
+ `title` ... 제목 
+ `content` ... 내용 
+ `author_id` ... 작성한 관리자 id

#### Response
+ `400` ... 필요한 파라메터가 제대로 오지 않았음
+ `401` ... 올바르지 않은 author_id 
+ `200` ... 성공

	```json
	{
	  "notifications": [
		{
		  "author": {
			"code": "abc", 
			"created_at": 1432073134.0, 
			"id": 1, 
			"name": "admin", 
			"updated_at": 1432073134.0, 
			"username": "admin123"
		  }, 
		  "author_id": 1, 
		  "content": "가나다라마$!@$asd12412D@!2", 
		  "created_at": 1432073155.0, 
		  "id": 1, 
		  "title": "noti1", 
		  "updated_at": 1432073155.0
		}
	  ]
	}
	```

#### Keys Description
+ `notifications` ... 공지사항들을 담은 list
	+ `notifiaction` ... 인자로 넘기지 않아도 리턴되는 값들
		+ `id` ... db 인덱스
		+ `author`... 글쓴이 객체
		+ `created_at (timestamp)` ... 작성 일자
		+ `updated_at (timestamp)` ... 업데이트 일자
		+ `title` ... 공지 제목
		+ `content` ... 공지 내용
		+ `author_id` ... 글쓴이 db 인덱스

# DELETE /notification/delete/\<idx>/
공지사항들 갱신하기

#### Header
+ 없음

#### Parameters
+ `title` ... 제목 
+ `content` ... 내용 
+ `author_id` ... 작성한 관리자 id

#### Response
+ `404` ... 필요한 파라메터가 제대로 오지 않았음
+ `505` ... 올바르지 않은 author_id 
+ `200` ... 성공

	```json
	{}
	```

#### Keys Description
+ 없음

# GET /point/\<username>\/
포인트 내 정보 보기

#### Header
+ `Content-Type` : `application/json`

#### Parameters
+ `password` ... 패스워드

#### Response
+ `200` ... 성공

	```json
	{
	  "user":
		{
		  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
		  "auth": false, 
		  "car_num": "4111", 
		  "created_at": 1432006370.0, 
		  "detail_address": "\u314e\u314e\u314e", 
		  "id": 1,
		  "point": 30000,
		  "regular_member": True,
		  "regular_at": 1432019572.0,
		  "main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
		  "name": "\uae40\uae40\uae40", 
		  "office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
		  "updated_at": 1432019572.0, 
		  "username": "kim0123"
		}
	}
	```

#### Keys Description
+ `user` ... 유저 객체
	+ `id` ... db 인덱스
	+ `name` ... 이름
	+ `username` ... 아이디
	+ `address` ... 통합 주소
	+ `main_address` ... 첫번째 주소
	+ `detail_address` ... 상세 주소
	+ `office` ... 소재지
	+ `auth` ... 승인 여부 
	+ `car_num` ... 차량 번호
	+ `point` ... 잔여 포인트
	+ `regular_member` ... 정회원 여부
	+ `regular_at` ... 등업 시기
	+ `created_at` ... 생성 시간 타임스탬프
	+ `updated_at` ... 업데이트 시간 타임스탬프

# POST /point/\<username>\/
포인트 충전하기

#### Header
+ `Content-Type` : `application/json`

#### Parameters
+ `password` ... 패스워드
+ `encrypt_key` ... 인증키 SHA1("sadari"+username)
+ `money` ... 충전할 가격

#### Response
+ `200` ... 성공

	```json
	{
	  "user":
		{
		  "address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9\u314e\u314e\u314e", 
		  "auth": false, 
		  "car_num": "4111", 
		  "created_at": 1432006370.0, 
		  "detail_address": "\u314e\u314e\u314e", 
		  "id": 1,
		  "point": 30000,
		  "regular_member": True,
		  "regular_at": 1432019572.0,
		  "main_address": "\uacbd\uae30\ub3c4 \ubd80\ucc9c\uc2dc \uc6d0\ubbf8\uad6c \uc0c1\ub3d9", 
		  "name": "\uae40\uae40\uae40", 
		  "office": "\ud558\uc778\u3139\uba38\u3163\u314f\u3139\ub2c8\ub9d0\ub2c8\u314f\u3141\ub9ac\u314f\u3141\u3134\u3147\ub9ac\u314f\u3141\ub2c8\u314f", 
		  "updated_at": 1432019572.0, 
		  "username": "kim0123"
		}
	}
	```
	
+ `400` ... 인자 오류
+ `401` ... 인증 오류 (패스워드 오류)
+ `403` ... 오더와 관련된 자 (등록자, 배차자) 가 아닌 경우
+ `404` ... 없는 오더
+ `409` ... 변경 불가능한 상태 변경을 요청할 경우 (ex. 등록자가 "작업중"을 "배차 대기"로 변경)


#### Keys Description
+ `user` ... 유저 객체
	+ `id` ... db 인덱스
	+ `name` ... 이름
	+ `username` ... 아이디
	+ `address` ... 통합 주소
	+ `main_address` ... 첫번째 주소
	+ `detail_address` ... 상세 주소
	+ `office` ... 소재지
	+ `auth` ... 승인 여부 
	+ `car_num` ... 차량 번호
	+ `point` ... 잔여 포인트
	+ `regular_member` ... 정회원 여부
	+ `regular_at` ... 등업 시기
	+ `created_at` ... 생성 시간 타임스탬프
	+ `updated_at` ... 업데이트 시간 타임스탬프