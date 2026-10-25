-- AlterTable
ALTER TABLE "closure_extensions" ADD COLUMN     "request_id" UUID NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "closure_extensions_request_id_key" ON "closure_extensions"("request_id");

