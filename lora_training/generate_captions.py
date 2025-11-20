import pandas as pd
import os

# ---------------------------------------------------------
# 설정 (Configuration)
# ---------------------------------------------------------
CSV_FILE = 'metadata.csv'       # 1. 관리하는 엑셀(CSV) 파일명
IMAGE_DIR = './images'          # 2. 이미지가 있는 폴더
CAPTION_DIR = './captions'      # 3. 캡션 파일이 저장될 폴더

# ---------------------------------------------------------
# 메인 로직
# ---------------------------------------------------------
def generate_captions():
    # 1. 캡션 저장 폴더가 없으면 생성
    os.makedirs(CAPTION_DIR, exist_ok=True)

    # 2. CSV 파일 로드
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"✅ '{CSV_FILE}' 로드 완료! 총 {len(df)}개의 데이터를 처리합니다.")
    except FileNotFoundError:
        print(f"❌ 오류: '{CSV_FILE}' 파일을 찾을 수 없습니다.")
        return

    success_count = 0

    # 3. 한 줄씩 읽어서 캡션 파일 생성
    for index, row in df.iterrows():
        filename = str(row['filename']).strip()
        
        # 확장자가 없으면 .jpg라고 가정하거나, 파일명만 쓴 경우 처리
        if '.' in filename:
            base_name = filename.rsplit('.', 1)[0]
        else:
            base_name = filename

        # [황금 순서 조합] 
        # 빈 칸이 있을 수 있으므로, 내용이 있는 것만 리스트로 모음
        parts = [
            row['trigger_word'],    # 1. 트리거
            row['subject'],         # 2. 피사체
            row['composition'],     # 3. 구도
            row['objective_desc'],  # 4. 객관적 묘사
            row['style_tags']       # 5. 스타일
        ]
        
        # 빈 값(NaN) 제거 및 문자열로 변환
        clean_parts = [str(p).strip() for p in parts if pd.notna(p) and str(p).strip() != '']
        
        # 쉼표(,)로 이어 붙여서 최종 캡션 완성
        final_caption = ", ".join(clean_parts)

        # .txt 파일로 저장
        txt_path = os.path.join(CAPTION_DIR, f"{base_name}.txt")
        
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(final_caption)
        
        success_count += 1

    print(f"🎉 완료! '{CAPTION_DIR}' 폴더에 총 {success_count}개의 캡션 파일이 생성되었습니다.")

if __name__ == "__main__":
    generate_captions()