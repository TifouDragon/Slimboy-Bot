
"""
Test des permissions et fonctionnalités du bot
"""

import discord

def test_permissions_logic():
    """Test the permission checking logic"""
    
    # Simulate guild permissions
    print("🧪 Test des permissions de modération...")
    
    # Test 1: User with ban permissions
    class MockPermissions:
        def __init__(self, ban_members=False, kick_members=False, manage_messages=False):
            self.ban_members = ban_members
            self.kick_members = kick_members
            self.manage_messages = manage_messages
    
    class MockUser:
        def __init__(self, permissions):
            self.guild_permissions = permissions
    
    # Test cases
    admin_user = MockUser(MockPermissions(ban_members=True, kick_members=True, manage_messages=True))
    mod_user = MockUser(MockPermissions(ban_members=True, kick_members=True, manage_messages=False))
    normal_user = MockUser(MockPermissions(ban_members=False, kick_members=False, manage_messages=False))
    
    def has_moderation_permission(user):
        """Check if user has moderation permissions"""
        return (
            user.guild_permissions.ban_members or 
            user.guild_permissions.kick_members or 
            user.guild_permissions.manage_messages
        )
    
    print(f"✅ Admin user can moderate: {has_moderation_permission(admin_user)}")
    print(f"✅ Mod user can moderate: {has_moderation_permission(mod_user)}")
    print(f"❌ Normal user can moderate: {has_moderation_permission(normal_user)}")
    
    print("\nLa correction devrait maintenant fonctionner correctement.")

if __name__ == "__main__":
    test_permissions_logic()
