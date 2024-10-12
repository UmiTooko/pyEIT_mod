# Hướng dẫn chạy pyEIT (mod)

## 0. Thư viện: 
Hãy cài python và các thư viện liên quan khác. Các thư viện đã được liệt kê trong requirement.txt và có thể chưa đủ, hãy tải các thứ viện còn thiếu trong quá trình chạy thử code, sử dụng `pip` để tải các thư viện về. Các bạn không cần tải thư viện pyEIT về, vì bản thân cái repo này đã có thư viện đó rồi.

Ví dụ: `pip install requirement.txt`; `pip install matplotlib`

## 1. Sơ lược:
Chương trình chính nằm ở file `main.py`. Chạy file `main.py` bằng cmd. Mở cmd và gõ `python main.py <Lệnh>` với `<Lệnh>` là các tổ hợplệnh được hỗ trợ, để biết có những lệnh gì hãy sử dụng `--help`. 

Ví dụ: `python main.py --help`

## 2. Tổng quan về main.py:
Chương trình sẽ đọc ma trận từ arduino qua PORT, đây là ma trận sai khác. Bên cạnh đó chương trình cũng đọc ma trận tham chiếu từ file data\ref.txt. Hai ma trận sẽ được xử lý và kết quả cuối cùng là hình ảnh khôi phục.

## 3. Danh sách và chú thích lệnh hỗ trợ:
-  `--help`            Mở hướng dẫn
-  `--port <port_name>`        Chỉ định cổng COM được kết nối với mạch, có thể vào Device Manager để biết tên cổng `<port_name>`, ví dụ "COM1", "COM2", "COM3"...
-  `--ref `             Sử dụng để lấy ma trận tham chiếu. Hãy dùng lệnh này khi chậu hoặc bất cứ vật chứa nào không có thể. Data sẽ được ghi vào file data/ref.txt. Đôi lúc data có thể bị ghi sai, khi đó hệ thống sẽ bão lỗi và cần phải được lấy ref lại.
- `--n_el <n_el>`          Số lượng điện cực, mặc định `n_el = 16`.
-  `--h0 <h0>`               Độ chia lưới, giá trị càng nhỏ ảnh càng chi tiết nhưng thời gian xử lý cao hơn. `<h0>` phải bé hơn 1, mặc định `<h0> = 0.06`,
-  `--p <p>`            Một tham số trong hàm Jacobian của thuật toán, mặc định `<p> = 0.2`. 
-  `--lamb <lambda>`    Một tham số khác, giá trị mặc định `<lambda> = 0.005`.
-  `--perm <perm>`             Giá trị độ điện thẩm, mặc định `<perm> = 10`.
-  `--norm`             Cố định mức 0 của colorbar với một giá trị bất kì, khá khó để tune và không khuyến khích dùng.
-  `--truth`            Đừng dùng cái lệnh này.
-  `--nor_dis_amp`      Cũng đừng dùng lệnh này. 
-  `--test`             Cũng đừng dùng lệnh này nốt.
-  `--static`           Tái tạo một ảnh duy nhất.
-  `--name <name>`             Đặt tên cho ảnh thu thập được, format tên là `<h0>_<p>_<lambda>_<name>.png` (Chỉ dùng với `--static` và `--ref`)
-  `--realtime`         Chạy thời gian thực, ảnh sẽ hiển thị liền kề nhau. Fps sẽ phụ thuộc vào giá trị `h0`, phương pháp khôi phục, tốc độ truyền tin của mạch và cả độ may mắn của bạn.
-  `--interval <i>`         Khoảng thời gian giữa từng frames một đơn vị ms, không phải `<i>` càng thấp fps càng cao, cách tune giá trị này sẽ được nói chi tiết ở phần sau.

Một vài ví dụ lệnh:
-  `python main.py --port COM8 --ref`      (Lấy reference data, cổng COM8)
-  `python main.py --port COM7 --n_el 32 --static`     (Vẽ ảnh cho hệ 32 điện cực)
-  `python main.py --port COM1 --h0 0.08 --lamb 0.002 --p 0.1 --static`    (Vẽ ảnh hệ 16 điện cực với các tham số h0 = 0.08, lambda = 0.002 và p = 0.1)
-  `python main.py --port COM2 --realtime --interval 200`      (Chạy realtime hệ 16 điện cực với khoảng cách giữa 2 lần đọc liên tiếp là 200ms)

## 4. Lưu ý 1: Các tham số Jacobian và h0:

`h0` càng nhỏ thì chia lưới càng chi tiết, hình sẽ sắc nét hơn nhưng thời gian chạy sẽ lâu. Về `p` và lambda, nhìn chung `p` nên lớn hơn `lambda`, và theo lý thuyết nếu `p` càng lớn và lambda càng nhỏ thì hình sẽ bị nhạy với nhiễu, còn nếu `p` với lambda sát nhau thì ảnh sẽ mượt hơn nhưng kích cỡ sẽ bị phình ra. Các bạn có thể chạy thử một vài cặp giá trị `p` và `lambda` để xem giá trị nào hợp với các bạn, vì nó còn phụ thuộc ít nhiều vào kích cỡ vật chứa, nước dùng trong vật chứa và may mắn của các bạn. Cơ sở lý thuyết của hai tham số này tương đối khó hiểu những được sử dụng tường minh trong code, các bạn có thể đọc hàm `solve()` trong file "pyeit/eit/base.py", hàm `setup()` của class JAC trong "pyeit/eit/jac.py" để biết thêm chi tiết.

## 5. Lưu ý 2: Về chạy realtime
Chúng mình từng cố phát triển một phương pháp "bắt tay" giữa mạch đo và máy tính, tức là mạch đo gửi tín hiệu lên cho máy tính khi nó đo xong và máy tính xử lý xong sẽ gửi trả tín hiệu. Làm như này sẽ tránh được hiện tượng ùn tắc ở cổng khi mà data đẩy lên quá nhanh nhưng máy tính xử lý quá chậm. Tuy nhiên do thiếu hụt kiến thức về giao thức UART, bọn mình chưa thực sự làm chủ được cái này. Nên nếu chưa thể phát triển được cái giao tiếp đó, hãy để thời gian gửi data của mạch gấp 2 đến 4 lần thời gian máy tính xử lý (quy định ở lệnh `--interval` đã đề cập bên trên), đây chỉ là trick và không phải một giải pháp hợp lý.

## 6. Lưu ý 3: Chạy với 2 file texts data.
File main.py chỉ được phát triển để chạy với 1 file ref.txt và data nhận từ bên ngoài vào. Nếu bạn muốn phân tích thuật toán, bạn có thể sử dụng file eit_dynamic_jac.py. Data của file này được lấy hoàn toàn từ 2 file texts nằm trong folder data, cụ thể là data/ref.txt và data/diff.txt. Data của 2 files này là ma trận m x n nỗi tiếp trên một hàng duy nhất (Các bạn có thể xem thử trong file .txt để hiểu rõ hơn), nếu copy data vào sẽ cần dành một vài giây để xóa xuống dòng, đưa toàn bộ data thành 1 dòng duy nhất.

## 7. Lưu ý 4: Một vài trivias:
- Thanh colorbar không thể cung cấp thông tin về độ dẫn điện tại vị trí đó, nó chỉ cho biết xu thế của độ dẫn điện (cao hay thấp). Realtime nếu enable colorbar sẽ bị bug tái tạo lại colorbar liên tục, mình chưa fix được cái này.
- Nếu bạn khôi phục hình ảnh và nhận thấy hình ảnh có một cái viền bao quanh vật thể của bạn, đây là ringing effect và Dev chính của thư viện này chưa thể xử lý triệt để được nó.
- Việc bấm tắt cửa số (x) trong realtime mode thỉnh thoảng có thể khiến cmd của IDe bị đơ (bọn mình dùng vscode). Hãy terminate thẳng terminal bằng tổ hợp phím CTRL+C.

## 8. Lưu ý 5: 
Nhìn chung, mình chưa làm chủ được thư viện này vì nó có rất nhiều những thuật toán khó đối với mình, cũng như mạch code class chồng chất class khá phức tạp, mình chỉ dám nhận là nắm được 30-40% thư viện này. Và sau một khoảng thời gian tương đối dài (cụ thể là hơn 1 năm) làm việc với pyEIT và EIDORS (Matlab), mình nhận thấy python hiệu suất tương đối lép vế so với EIDORS của Matlab, có thể là do 2 thư viện được phát triển khác nhau và EIDORS được phát triển tốt hơn, hoặc bản thân Python có hiệu suất xử lý chưa bằng Matlab, hoặc là do mình chưa thể tối ưu thư viện pyEIT này. Mình khuyên các bạn cũng nên thử nghiên cứu EIDORS để có thể có được những kết quả tốt nhất. Cuối cùng chương trình có thể vẫn còn bug do đã lâu ngày mình chưa chạy lại, hãy liên hệ nếu bạn cần thêm thông tin.