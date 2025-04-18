DECLARE @username varchar(25) = ?;
DECLARE @password varchar(50) = ?;
DECLARE @IP varchar(max) = ?;
DECLARE @result bit = 0;

BEGIN TRY
    IF NOT EXISTS (SELECT 1 FROM TB_User WHERE StrUserID = @username)
    BEGIN
        INSERT INTO TB_User (StrUserID, password, regtime, reg_ip, sec_primary, sec_content)
        VALUES (@username, @password, GETDATE(), @IP, 3, 3)
        SET @result = 1;
    END
    ELSE IF EXISTS (SELECT 1 FROM TB_User WHERE StrUserID = @username AND password = @password)
    BEGIN
        SET @result = 1; -- Kullanıcı zaten var ve şifre doğru
    END

    SELECT @result AS success, @username AS username;
END TRY
BEGIN CATCH
    SELECT 0 AS success, @username AS username, ERROR_MESSAGE() AS error_message;
END CATCH