-- CreateEnum
CREATE TYPE "DataReportResolver" AS ENUM ('OWNER', 'ADMIN');

-- AlterTable
ALTER TABLE "data_reports" ADD COLUMN     "resolved_as" "DataReportResolver";

-- CreateIndex
CREATE UNIQUE INDEX "data_reports_open_key" ON "data_reports"("user_id", "space_id", "field") WHERE ("status" = 'OPEN');

