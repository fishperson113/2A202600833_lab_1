# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Khi temperature thấp, câu trả lời thường ổn định, ngắn gọn và ít biến thể. Khi temperature tăng, câu trả lời bắt đầu đa dạng hơn về cách diễn đạt, có thể thêm ví dụ hoặc góc nhìn mới, nhưng cũng dễ lan man hơn. Nói ngắn gọn: temperature càng cao thì tính sáng tạo càng tăng, còn độ nhất quán giảm.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Mình sẽ chọn khoảng 0.2 đến 0.4. Mức này đủ thấp để câu trả lời ổn định, đúng trọng tâm và ít rủi ro bịa đặt, nhưng vẫn không quá cứng nhắc như temperature 0.0.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Với cùng lượng token đầu ra, GPT-4o đắt hơn GPT-4o-mini khoảng 16.7 lần, vì $0.010 / 0.0006 \approx 16.7$. Số người dùng hay số lần gọi API không làm đổi tỷ lệ này nếu chỉ so chi phí output per token.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> GPT-4o xứng đáng khi cần suy luận khó, trả lời nhiều bước, hoặc độ chính xác/ngữ cảnh rất quan trọng như hỗ trợ kỹ thuật phức tạp. GPT-4o-mini phù hợp hơn cho tác vụ thông thường như FAQ, phân loại, tóm tắt ngắn, hoặc chatbot có khối lượng lớn và cần tối ưu chi phí.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất khi người dùng cần thấy phản hồi ngay lập tức, ví dụ chatbot tương tác, trợ lý viết nội dung, hoặc các câu trả lời dài vì nó cải thiện cảm nhận tốc độ và trải nghiệm chờ đợi. Non-streaming phù hợp hơn khi đầu ra ngắn, khi cần xử lý trọn vẹn trước rồi mới hiển thị, hoặc khi ứng dụng ưu tiên đơn giản hóa logic và không cần cập nhật theo từng token.


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
