from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler

from application.usecase.post_camp_gear_sale_use_case import PostCampGearSaleUseCase
from infrastructure.repository.product_repository import ProductRepository
from infrastructure.service.product_service import ProductService
from infrastructure.service.post_service import PostService


load_dotenv()


def main():
    product_repository = ProductRepository(ProductService())
    post_service = PostService()

    post_camp_gear_sale_use_case = PostCampGearSaleUseCase(
        product_repository, post_service
    )

    scheduler = BlockingScheduler(timezone="Asia/Tokyo")
    scheduler.add_job(post_camp_gear_sale_use_case.handle, "interval", minutes=30)
    scheduler.start()


if __name__ == "__main__":
    main()
