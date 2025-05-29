SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[report_comments](
	[commentid] int IDENTITY(1,1) PRIMARY KEY,
	[commentdatetime] [datetime] NULL,
	[user_id] [varchar](100) NULL,
	[sales_po] [varchar](100) NULL,
	[comment] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
