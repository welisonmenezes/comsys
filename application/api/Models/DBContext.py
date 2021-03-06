from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, Table, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

Post_Term = Table('Post_Term', Base.metadata,
    Column('post_id', Integer, ForeignKey('Post.id', name='fk_post_term_post_id'), nullable=False),
    Column('term_id', Integer, ForeignKey('Term.id', name='fk_post_term_term_id'), nullable=False)
)

Post_Type_Taxonomy = Table('Post_Type_Taxonomy', Base.metadata,
    Column('post_type_id', Integer, ForeignKey('Post_Type.id', name='fk_post_type_taxonomy_post_type_id'), nullable=False),
    Column('taxonomy_id', Integer, ForeignKey('Taxonomy.id', name='fk_post_type_taxonomy_taxonomy_id'), nullable=False)
)

Sector_Menu = Table('Sector_Menu', Base.metadata,
    Column('sector_id', Integer, ForeignKey('Sector.id', name='fk_sector_menu_sector_id'), nullable=False),
    Column('menu_id', Integer, ForeignKey('Menu.id', name='fk_sector_menu_menu_id'), nullable=False)
)

Capability_Role = Table('Capability_Role', Base.metadata,
    Column('capability_id', Integer, ForeignKey('Capability.id', name='fk_capability_role_capability_id'), nullable=False),
    Column('role_id', Integer, ForeignKey('Role.id', name='fk_capability_role_role_id'), nullable=False)
)

class Blacklist(Base):
    __tablename__ = 'Blacklist'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False) # must be what kind of item is (email, ip,  user, etc...)
    value = Column(Text, nullable=False)
    target = Column(String(100), nullable=False) # must be what kind of element will be protected (login, comments, etc...)


class Capability(Base):
    __tablename__ = 'Capability'
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=True)
    type = Column(String(50), nullable=False) # what will access specifically (single-post, post-type, menu, user, etc...)
    target_id = Column(Integer, nullable=True) # specifc post and post_type id if type is single-post or post-type
    can_write = Column(Boolean, nullable=False)
    can_read = Column(Boolean, nullable=False)
    can_delete = Column(Boolean, nullable=False)
    only_themselves = Column(Boolean, nullable=False)
    # relationships
    roles = relationship('Role', secondary=Capability_Role)


class Comment(Base):
    __tablename__ = 'Comment'
    id = Column(Integer, primary_key=True)
    comment = Column(Text, nullable=False)
    status = Column(String(15), nullable=False)
    origin_ip = Column(String(100), nullable=False)
    origin_agent = Column(String(255), nullable=False)
    created = Column(DateTime, nullable=False)
    # foreignKeys
    parent_id = Column(Integer, ForeignKey('Comment.id', name='fk_comment_parent_id'), nullable=True)
    user_id = Column(Integer, ForeignKey('User.id', name='fk_comment_user_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id', name='fk_comment_post_id'), nullable=False)
    language_id = Column(Integer, ForeignKey('Language.id', name='fk_comment_language_id'), nullable=False)
    # relationships
    user = relationship('User', foreign_keys='Comment.user_id')
    language = relationship('Language', foreign_keys='Comment.language_id')
    post = relationship('Post', foreign_keys='Comment.post_id')
    parent = relationship('Comment', foreign_keys='Comment.parent_id', remote_side='Comment.id')
    children = relationship('Comment')


class Configuration(Base):
    __tablename__ = 'Configuration'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    has_comments = Column(Boolean, nullable=False)
    email = Column(String(100), nullable=True)
    # foreignKeys
    language_id = Column(Integer, ForeignKey('Language.id', name='fk_configuration_language_id'), nullable=False)
    # relationships
    language = relationship('Language', foreign_keys='Configuration.language_id')
    socials = relationship('Social', foreign_keys='Social.configuration_id')


class Field(Base):
    __tablename__ = 'Field'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    type = Column(String(15), nullable=False) # can be content, text and file
    order = Column(Integer, nullable=False)
    # foreignKeys
    grouper_id = Column(Integer, ForeignKey('Grouper.id', name='fk_field_grouper_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id', name='fk_field_post_id'), nullable=False)
    # relationships
    grouper = relationship('Grouper', foreign_keys='Field.grouper_id')
    post = relationship('Post', foreign_keys='Field.post_id')
    field_file = relationship('FieldFile', uselist=False)
    field_content = relationship('FieldContent', uselist=False)
    # texts = relationship('FieldText')


class FieldContent(Base):
    __tablename__ = 'Field_Content'
    id = Column(Integer, primary_key=True)
    content = Column(Text(4294000000), nullable=False)
    # foreignKeys
    field_id = Column(Integer, ForeignKey('Field.id', name='fk_field_content_field_id'), nullable=False)
    grouper_id = Column(Integer, ForeignKey('Grouper.id', name='fk_field_content_grouper_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id', name='fk_field_content_post_id'), nullable=False)
    # relationships
    #field = relationship('Field', foreign_keys='FieldContent.field_id')


class FieldFile(Base):
    __tablename__ = 'Field_File'
    id = Column(Integer, primary_key=True)
    # foreignKeys
    field_id = Column(Integer, ForeignKey('Field.id', name='fk_field_file_field_id'), nullable=False)
    media_id = Column(Integer, ForeignKey('Media.id', name='fk_field_file_media_id'), nullable=False)
    grouper_id = Column(Integer, ForeignKey('Grouper.id', name='fk_field_file_grouper_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id', name='fk_field_file_post_id'), nullable=False)
    # relationships
    media = relationship('Media', foreign_keys='FieldFile.media_id')
    #field = relationship('Field', foreign_keys='FieldFile.field_id')


class FieldText(Base):
    __tablename__ = 'Field_Text'
    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    # foreignKeys
    field_id = Column(Integer, ForeignKey('Field.id', name='fk_field_text_field_id'), nullable=False)
    grouper_id = Column(Integer, ForeignKey('Grouper.id', name='fk_field_text_grouper_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('Post.id', name='fk_field_text_post_id'), nullable=False)
    # relationships
    #field = relationship('Field', foreign_keys='FieldText.field_id')


class Grouper(Base):
    __tablename__ = 'Grouper'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    order = Column(Integer, nullable=False)
    # foreignKeys
    parent_id = Column(Integer, ForeignKey('Grouper.id', name='fk_grouper_parent_id'), nullable=True)
    post_id = Column(Integer, ForeignKey('Post.id', name='fk_grouper_post_id'), nullable=False)
    # relationships
    parent = relationship('Grouper', foreign_keys='Grouper.parent_id', remote_side='Grouper.id')
    children = relationship('Grouper')
    post = relationship('Post', foreign_keys='Grouper.post_id')
    fields = relationship('Field')
    

class Language(Base):
    __tablename__ = 'Language'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(10), nullable=False, unique=True)
    status = Column(String(15), nullable=False)
    datetime_format = Column(String(100), nullable=True) # must be an regular expression
    # relationships
    #posts = relationship('Post')
    #terms = relationship('Term')
    #configurations = relationship('Configuration')
    #comments = relationship('Comment')
    #menus = relationship('Menu')


class Media(Base):
    __tablename__ = 'Media'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    type = Column(String(100), nullable=False)
    extension = Column(String(4), nullable=False)
    file = Column(LargeBinary(length=(2**24)-1), nullable=False)
    origin = Column(String(50), nullable=False) # where came from (post, user avatar, configuration, etc...)
    created = Column(DateTime, nullable=False)
    # foreignKeys
    user_id = Column(Integer, ForeignKey('User.id', name='fk_media_user_id'), nullable=False)
    # relationships
    user = relationship('User', foreign_keys='Media.user_id')
    #avatar_owner = relationship('User', foreign_keys='User.avatar_id')
    #field_files = relationship('FieldFile')


class Menu(Base):
    __tablename__ = 'Menu'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    order = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    # foreignKeys
    language_id = Column(Integer, ForeignKey('Language.id', name='fk_menu_language_id'), nullable=False)
    # relationships
    language = relationship('Language', foreign_keys='Menu.language_id')
    sectors = relationship('Sector', secondary=Sector_Menu)
    items = relationship('MenuItem')


class MenuItem(Base):
    __tablename__ = 'Menu_Item'
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False) # can be anchor, external link, link, etc...
    behavior = Column(String(50), nullable=False) # what window will be opened
    url = Column(String(255), nullable=True)
    target_id = Column(Integer, nullable=True)
    title = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False)
    # foreignKeys
    parent_id = Column(Integer, ForeignKey('Menu_Item.id', name='fk_menu_item_parent_id'), nullable=True)
    menu_id = Column(Integer, ForeignKey('Menu.id', name='fk_menu_item_menu_id'), nullable=False)
    # relationships
    parent = relationship('MenuItem', foreign_keys='MenuItem.parent_id', remote_side='MenuItem.id')
    children = relationship('MenuItem')
    menu = relationship('Menu', foreign_keys='MenuItem.menu_id')


class Nest(Base):
    __tablename__ = 'Nest'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    limit = Column(Integer, nullable=False, default=0)
    has_pagination = Column(Boolean, nullable=False)
    # foreignKeys
    post_id = Column(Integer, ForeignKey('Post.id', name='fk_nest_post_id'), nullable=False)
    post_type_id = Column(Integer, ForeignKey('Post_Type.id', name='fk_nest_post_type_id'), nullable=False)
    # relationships
    post = relationship('Post', foreign_keys='Nest.post_id')
    post_type = relationship('PostType', foreign_keys='Nest.post_type_id')


class Post(Base):
    __tablename__ = 'Post'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True) # unique name/url path
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(15), nullable=False)
    is_protected = Column(Boolean, nullable=False) # if will be accessable to read without login
    has_comments = Column(Boolean, nullable=False)
    publish_on = Column(DateTime, nullable=True)
    expire_on = Column(DateTime, nullable=True)
    created = Column(DateTime, nullable=False)
    edited = Column(DateTime, nullable=False)
    # foreignKeys
    parent_id = Column(Integer, ForeignKey('Post.id', name='fk_post_parent_id'), nullable=True)
    post_type_id = Column(Integer, ForeignKey('Post_Type.id', name='fk_post_post_type_id'), nullable=False)
    language_id = Column(Integer, ForeignKey('Language.id', name='fk_post_language_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id', name='fk_post_user_id'), nullable=False)
    # relationships
    terms = relationship('Term', secondary=Post_Term)
    parent = relationship('Post', foreign_keys='Post.parent_id', remote_side='Post.id')
    children = relationship('Post')
    post_type = relationship('PostType', foreign_keys='Post.post_type_id')
    user = relationship('User', foreign_keys='Post.user_id')
    language = relationship('Language', foreign_keys='Post.language_id')
    nests = relationship('Nest')
    groupers = relationship('Grouper')
    terms = relationship('Term', secondary=Post_Term)
    # comments = relationship('Comment')
    #page_owner = relationship('User', foreign_keys='User.page_id')


class PostType(Base):
    __tablename__ = 'Post_Type'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    type = Column(String(50), nullable=False) # if the page will be to nest, user, tax, post, static, etc.
    # foreignKeys
    template_id = Column(Integer, ForeignKey('Template.id', name='fk_post_type_template_id'))
    # relationships
    template = relationship('Template', foreign_keys='PostType.template_id')
    nests = relationship('Nest')
    taxonomies = relationship('Taxonomy', secondary=Post_Type_Taxonomy)
    # posts = relationship('Post')


class Role(Base):
    __tablename__ = 'Role'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    can_access_admin = Column(Boolean, nullable=False)
    # relationships
    capabilities = relationship('Capability', secondary=Capability_Role)
    #users = relationship('User')


class Sector(Base):
    __tablename__ = 'Sector'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    # relationships
    menus = relationship('Menu', secondary=Sector_Menu)


class Social(Base):
    __tablename__ = 'Social'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(255), nullable=False)
    target = Column(String(15), nullable=True)
    description = Column(String(255), nullable=True)
    origin = Column(String(50), nullable=False)
    # foreignKeys
    configuration_id = Column(Integer, ForeignKey('Configuration.id', name='fk_social_configuration_id'), nullable=True)
    user_id = Column(Integer, ForeignKey('User.id', name='fk_social_user_id'), nullable=True)
    # relationships
    configuration = relationship('Configuration', foreign_keys='Social.configuration_id')
    user = relationship('User', foreign_keys='Social.user_id')


class Taxonomy(Base):
    __tablename__ = 'Taxonomy'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    has_child = Column(Boolean, nullable=False) # if will have hierarchy
    # relationships
    post_types = relationship('PostType', secondary=Post_Type_Taxonomy)
    terms = relationship('Term')


class Template(Base):
    __tablename__ = 'Template'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    value = Column(Text(4294000000), nullable=False) # will have a json configuration structure
    # relationships
    post_types = relationship('PostType')


class Term(Base):
    __tablename__ = 'Term'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    # foreignKeys
    parent_id = Column(Integer, ForeignKey('Term.id', name='fk_term_parent_id'), nullable=True)
    page_id = Column(Integer, ForeignKey('Post.id', name='fk_term_page_id'), nullable=True) # the term's custom page
    taxonomy_id = Column(Integer, ForeignKey('Taxonomy.id', name='fk_term_taxonomy_id'), nullable=False)
    language_id = Column(Integer, ForeignKey('Language.id', name='fk_term_language_id'), nullable=False)
    # relationships
    parent = relationship('Term', foreign_keys='Term.parent_id', remote_side='Term.id')
    children = relationship('Term')
    language = relationship('Language', foreign_keys='Term.language_id')
    posts = relationship('Post', secondary=Post_Term)
    taxonomy = relationship('Taxonomy', foreign_keys='Term.taxonomy_id')
    # page = relationship('Post', foreign_keys='Term.page_id')


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    login = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    nickname = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=False)
    registered = Column(DateTime, nullable=False)
    status = Column(String(15), nullable=False)
    refresh_token = Column(String(400), nullable=True)
    # foreignKeys
    role_id = Column(Integer, ForeignKey('Role.id', name='fk_user_role_id'), nullable=False)
    avatar_id = Column(Integer, ForeignKey('Media.id', name='fk_user_avatar_id'), nullable=True)
    page_id = Column(Integer, ForeignKey('Post.id', name='fk_user_page_id'), nullable=True)
    # relationships
    role = relationship('Role', foreign_keys='User.role_id')
    socials = relationship('Social', foreign_keys='Social.user_id')
    medias = relationship('Media', foreign_keys='Media.user_id')
    page = relationship('Post', foreign_keys='User.page_id')
    avatar = relationship('Media', foreign_keys='User.avatar_id')
    #posts = relationship('Post', foreign_keys='Post.user_id')
    #comments = relationship('Comment')


class Variable(Base):
    __tablename__ = 'Variable'
    id = Column(Integer, primary_key=True)
    key = Column(String(255), nullable=False, unique=True)
    value = Column(Text(4294000000), nullable=False)