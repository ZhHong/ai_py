#ifndef _TEACRYPTH_
#define _TEACRYPTH_
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <string>

#define P 0xffffffffffffffc5ull
#define G 5

namespace Crypt {

	static const std::string base64_chars =
		"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		"abcdefghijklmnopqrstuvwxyz"
		"0123456789+/";


	static inline bool is_base64(unsigned char c) {
		return (isalnum(c) || (c == '+') || (c == '/'));
	}

	inline std::string base64_encode(unsigned char const* bytes_to_encode, unsigned int in_len) {
		std::string ret;
		int i = 0;
		int j = 0;
		unsigned char char_array_3[3];
		unsigned char char_array_4[4];

		while (in_len--) {
			char_array_3[i++] = *(bytes_to_encode++);
			if (i == 3) {
				char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
				char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
				char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
				char_array_4[3] = char_array_3[2] & 0x3f;

				for (i = 0; (i <4); i++)
					ret += base64_chars[char_array_4[i]];
				i = 0;
			}
		}

		if (i)
		{
			for (j = i; j < 3; j++)
				char_array_3[j] = '\0';

			char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
			char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
			char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
			char_array_4[3] = char_array_3[2] & 0x3f;

			for (j = 0; (j < i + 1); j++)
				ret += base64_chars[char_array_4[j]];

			while ((i++ < 3))
				ret += '=';

		}

		return ret;

	}

	inline std::string base64_decode(std::string const& encoded_string) {
		int in_len = encoded_string.size();
		int i = 0;
		int j = 0;
		int in_ = 0;
		unsigned char char_array_4[4], char_array_3[3];
		std::string ret;

		while (in_len-- && (encoded_string[in_] != '=') && is_base64(encoded_string[in_])) {
			char_array_4[i++] = encoded_string[in_]; in_++;
			if (i == 4) {
				for (i = 0; i <4; i++)
					char_array_4[i] = base64_chars.find(char_array_4[i]);

				char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
				char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
				char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

				for (i = 0; (i < 3); i++)
					ret += char_array_3[i];
				i = 0;
			}
		}

		if (i) {
			for (j = i; j <4; j++)
				char_array_4[j] = 0;

			for (j = 0; j <4; j++)
				char_array_4[j] = base64_chars.find(char_array_4[j]);

			char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
			char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
			char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

			for (j = 0; (j < i - 1); j++) ret += char_array_3[j];
		}

		return ret;
	}

	inline uint64_t mul_mod_p(uint64_t a, uint64_t b) {
		uint64_t m = 0;
		while (b) {
			if (b & 1) {
				uint64_t t = P - a;
				if (m >= t) {
					m -= t;
				}
				else {
					m += a;
				}
			}
			if (a >= P - a) {
				a = a * 2 - P;
			}
			else {
				a = a * 2;
			}
			b >>= 1;
		}
		return m;
	}

	inline uint64_t pow_mod_p(uint64_t a, uint64_t b) {
		if (b == 1) {
			return a;
		}
		uint64_t t = pow_mod_p(a, b >> 1);
		t = mul_mod_p(t, t);
		if (b % 2) {
			t = mul_mod_p(t, a);
		}
		return t;
	}

	// calc a^b % p
	inline uint64_t powmodp(uint64_t a, uint64_t b) {
		if (a == 0)
			return 1;
		if (b == 0)
			return 1;
		if (a > P)
			a %= P;
		return pow_mod_p(a, b);
	}

	inline void dh64_key_pair(uint64_t* private_key, uint64_t* public_key) {
		uint64_t a = rand();
		uint64_t b = rand() & 0xFFFF;
		uint64_t c = rand() & 0xFFFF;
		uint64_t d = (rand() & 0xFFFF) + 1;
		*private_key = a << 48 | b << 32 | c << 16 | d;
		*public_key = powmodp(G, *private_key);
	}

	inline  uint64_t dh64_public_key(const uint64_t private_key) {
		return powmodp(G, private_key);
	}

	inline  uint64_t dh64_secret(const uint64_t private_key, const uint64_t another_public_key) {
		return powmodp(another_public_key, private_key);
	}

	inline	void encrypt(uint32_t v[], uint32_t k[]) {
		uint32_t v0 = v[0], v1 = v[1], sum = 0, i;           /* set up */
		uint32_t delta = 0x9e3779b9;                     /* a key schedule constant */
		uint32_t k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];   /* cache key */
		for (i = 0; i < 32; i++) {                       /* basic cycle start */
			sum += delta;
			v0 += ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1);
			v1 += ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3);
		}                                              /* end cycle */
		v[0] = v0; v[1] = v1;
	}

	inline	void decrypt(uint32_t v[], uint32_t k[]) {
		uint32_t v0 = v[0], v1 = v[1], sum = 0xC6EF3720, i;  /* set up */
		uint32_t delta = 0x9e3779b9;                     /* a key schedule constant */
		uint32_t k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];   /* cache key */
		for (i = 0; i<32; i++) {                         /* basic cycle start */
			v1 -= ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3);
			v0 -= ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1);
			sum -= delta;
		}                                              /* end cycle */
		v[0] = v0; v[1] = v1;
	}

	inline uint64_t hexToDec(std::string hexstr) {
		uint64_t sum = 0;
		int count = hexstr.length();
		for (int i = count - 1; i >= 0; i--)
		{
			if (hexstr[i] >= '0'&&hexstr[i] <= '9')
			{
				sum += (hexstr[i] - 48)*(uint64_t)pow(16, count - i - 1);
			}
			else if (hexstr[i] >= 'A'&&hexstr[i] <= 'F') 
			{
				sum += (hexstr[i] - 55)*(uint64_t)pow(16, count - i - 1);
			}
		}
		return sum;
	}

	/**
	return HEX_STRING
	**/
	inline void GenKey(std::string *public_key_str, std::string *private_key_str) {
		uint64_t public_key;
		uint64_t private_key;
		dh64_key_pair(&private_key, &public_key);
		char p1[32], p2[32];
		sprintf_s(p1, 32, "%016llX", public_key);
		sprintf_s(p2, 32, "%016llX", private_key);
		*public_key_str = p1;
		*private_key_str = p2;
	}
	/**
	return secret
	**/
	inline void GenSecret(std::string public_key, std::string private_key, std::string &secret) {
		uint64_t pub_key = hexToDec(public_key);
		uint64_t pri_key = hexToDec(private_key);
		uint64_t sec = dh64_secret(pri_key, pub_key);
		char p[32];
		sprintf_s(p, 32, "%016llX", sec);
		secret = p;
	}

	/**
	encrypto
	**/
	inline void Encrypt(std::string &text, std::string secret) {
		int secret_length = secret.length();
		int text_length = text.length();
		uint32_t k[16];
		for (int i = 0; i < secret_length; ++i) {
			k[i] = secret[i];
		}
		uint32_t v[1024];
		for (int i = 0; i < 1024; ++i) {
			if (i >= text_length) {
				v[i] = 0;
			}
			else {
				v[i] = text[i];
			}
		}
		for (int m = 0; m < text_length; m += 2) {
			uint32_t tempvalue[2] = { v[m],v[m + 1] };
			for (int i = 0; i < secret_length; i += 4) {
				uint32_t tempkey[4] = { k[i],k[i + 1],k[i + 2],k[i + 3] };
				encrypt(tempvalue, tempkey);
			}
			v[m] = tempvalue[0];
			v[m + 1] = tempvalue[1];
		}
		text = "";
		for (int i = 0; i <= text_length; ++i) {
			char p[32];
			sprintf_s(p, 32, "%08X", v[i]);
			text += p;
		}
	}
	/**
	decrypto
	**/
	inline void Decrypt(std::string &text, std::string secret) {
		int secret_length = secret.length();
		int text_length = text.length();
		const int num_v = text_length / 8;

		uint32_t k[16];
		for (int i = 0; i < secret_length; ++i) {
			k[i] = secret[i];
		}
		static uint32_t vv[1024];
		int j = 0;
		for (int i = 0; i <= text_length; ) {
			std::string value = text.substr(i, 8);
			uint32_t value1 = hexToDec(value);
			vv[j] = value1;
			j += 1;
			i += 8;
		}
		for (int m = 0; m < num_v; m += 2) {
			uint32_t tempvalue[2] = { vv[m],vv[m + 1] };
			for (int i = secret_length - 1; i > 0; i -= 4) {
				uint32_t tempkey[4] = { k[i - 3],k[i - 2],k[i - 1],k[i] };
				decrypt(tempvalue, tempkey);
			}
			vv[m] = tempvalue[0];
			vv[m + 1] = tempvalue[1];
		}
		text = "";
		char arr[1024];
		int i = 0;
		for (i; i < num_v; ++i) {
			arr[i] = vv[i];
		}
		arr[num_v - 1] = 0;
		text = arr;
	}

	inline void GetPublicKey(std::string &public_key, std::string private_key) {
		uint64_t pri_key = hexToDec(private_key);
		uint64_t pub_key = dh64_public_key(pri_key);
		char p[32];
		sprintf_s(p, 32, "%016llX", pub_key);
		public_key = p;
	}
}
#endif