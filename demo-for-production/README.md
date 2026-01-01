# Order for production ready
## For demo-n-tier after code have already available
Phase 1 - MVP:
1. Authen/Author
2. Database (postgres)
3. Error handling
4. Basic testing
5. Docket setup

Phase 2 - Production-ready:

6. CI/CD
7. Monitoring & alerting
8. Caching & performance
9. Security hardening

Phase 3 - Scale:

10. Load balancing
11. Auto scaling

## Tại sao cần setup docker:
Docker đảm bảo ứng dụng chạy nhất quán ở mọi môi trường, cô lập dependency, dễ scale và deploy. Thay cài đặt thủ công, chỉ cần chạy `docker run` với image đã built sẵn.

Ngoài ra, nó còn rất quan trọng trong việc setup CI/CD